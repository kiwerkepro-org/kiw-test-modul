<?php
/**
 * Admin Pingback Service.
 *
 * @package KIW\Module\Template\Admin
 */

declare(strict_types=1);

namespace KIW\Module\Template\Admin;

// Ergänzung: Import der Proxy-Klasse für die sichere Kommunikation
use KIW\Module\Utils\ProxyRequest;

/**
 * Class Pingback
 * * Sends "I am alive" signals and handles admin notices independently of WP Cron.
 */
final class Pingback
{
    /**
     * Initialize Pingback.
     */
    public function __construct()
    {
        // Hook into admin init to check status
        add_action('admin_init', [$this, 'checkStatus']);
    }

    /**
     * Check Status.
     * * Runs on admin_init to verify system health.
     *
     * @return void
     */
    public function checkStatus(): void
    {
        // Example logic: Check if a transient is expired implies we haven't checked in.
        if (false === get_transient('kiw_module_template_ping')) {
            $this->sendPing();
            set_transient('kiw_module_template_ping', 'alive', 12 * HOUR_IN_SECONDS);
        }
    }

    /**
     * Send Ping.
     * * Logs status or sends to central dashboard.
     *
     * @return void
     */
    private function sendPing(): void
    {
        // ERGÄNZUNG: Realisierung des Integritäts-Handshakes mit der KI-WERKE CENTRAL
        $checksum_path = plugin_dir_path(__DIR__) . '../checksums.json';
        $build_hash    = 'unknown';

        if (file_exists($checksum_path)) {
            $checksum_data = json_decode(file_get_contents($checksum_path), true);
            $build_hash    = $checksum_data['release_hash'] ?? 'no_hash_found';
        }

        // Aufruf über die neue ProxyRequest Klasse (inkl. Basic Auth Schutz)
        ProxyRequest::call('https://zentrale.kiwerke.com/api/v1/verify', [
            'method' => 'POST',
            'body'   => [
                'action'   => 'integrity_heartbeat',
                'module'   => 'kiw-module-template', // Wird im konkreten Modul angepasst
                'version'  => '1.1.0',
                'hash'     => $build_hash,
                'site_url' => get_site_url()
            ]
        ]);
    }
}