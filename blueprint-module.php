<?php
/**
 * Module Blueprint: Test Modul
 * Logic and View are strictly separated according to architecture.md.
 */

defined('ABSPATH') || exit;

// ==========================================================================
// 1. LOGIC SECTION (Data Processing, Hooks, APIs)
// ==========================================================================

function kiw_module_template_logic() {
    // Hier nur PHP-Logik, keine HTML-Ausgabe
    $data = [
        'title' => esc_html__('Test Modul', 'kiw-test-modul'),
        'status' => 'active'
    ];
    
    return $data;
}

// ==========================================================================
// 2. VIEW SECTION (HTML & Tailwind Output)
// ==========================================================================

$view_path = plugin_dir_path(__FILE__) . 'views/blueprint-view.php';

if (file_exists($view_path)) {
    include $view_path;
} else {
    echo '<div class="notice notice-error"><p>' . esc_html__('Fehler: Blueprint-View nicht gefunden.', 'kiw-test-modul') . '</p></div>';
}