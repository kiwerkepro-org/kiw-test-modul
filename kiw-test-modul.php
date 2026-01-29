<?php
/**
 * Plugin Name: Test Modul
 * Description: Template for KIW private module distribution.
 * Version: 0.1.0
 * Author: KIW
 * License: GPLv2 or later
 * Text Domain: kiw-test-modul
 */

declare(strict_types=1);

namespace KIW\TestModul;

defined('ABSPATH') || exit;

// Define dynamic constants (Path/URL require function calls, so keep as define or static properties)
define('KIW_TEST_MODUL_PATH', plugin_dir_path(__FILE__));
define('KIW_TEST_MODUL_URL', plugin_dir_url(__FILE__));

final class Core {
    // PHP 8.3 Typed Constants
    public const string VERSION = '0.1.0';
    public const string MIN_PHP_VERSION = '8.3';
    public const string MIN_WP_VERSION = '6.0';
    public const string SLUG = 'kiw-test-modul';

    public static function init(): void {
        // Compatibility Check
        if (!self::check_compatibility()) {
            return;
        }

        // Admin-Menü Registrierung
        add_action('admin_menu', [self::class, 'register_menu']);
    }

    private static function check_compatibility(): bool {
        if (version_compare(phpversion(), self::MIN_PHP_VERSION, '<')) {
            add_action('admin_notices', function(): void {
                echo '<div class="notice notice-error"><p>' 
                     . esc_html(sprintf(__('Module requires PHP %s or higher.', 'kiw-test-modul'), self::MIN_PHP_VERSION)) 
                     . '</p></div>';
            });
            return false;
        }
        return true;
    }

    public static function register_menu(): void {
        if (!current_user_can('manage_options')) {
            return;
        }

        add_management_page(
            __('Test Modul', self::SLUG),
            __('Test Modul', self::SLUG),
            'manage_options',
            self::SLUG,
            [self::class, 'render_page']
        );
    }

    /**
     * Loads the dashboard following architecture.md standards.
     */
    public static function render_page(): void {
        if (!current_user_can('manage_options')) {
            return;
        }

        // Optimierte File-Path-Auflösung (Performance Agent)
        $view_path = KIW_TEST_MODUL_PATH . 'views/admin-dashboard.php';

        if (file_exists($view_path)) {
            require_once $view_path;
        } else {
            echo '<div class="notice notice-error"><p>' . esc_html__('View not found.', self::SLUG) . '</p></div>';
        }
    }
}

// Boot
Core::init();