<?php
namespace KIW\Module\Utils;

/**
 * KI-WERKE Proxy Gatekeeper
 * Leitet alle externen API-Anfragen über die Zentrale.
 */
class ProxyRequest {
    
    // Die Public Gateway URL deiner Zentrale
    private static $zentrale_url = 'https://zentrale.kiwerke.com/api/v1/proxy';

    /**
     * Führt einen sicheren API-Call über den Zentrale-Proxy aus.
     */
    public static function call($target_url, $args = []) {
        // Authentifizierung via Umgebungsvariablen oder Konstanten (.env)
        $auth_user = defined('KIW_CENTRAL_USER') ? KIW_CENTRAL_USER : getenv('KIW_CENTRAL_USER');
        $auth_pass = defined('KIW_CENTRAL_PASS') ? KIW_CENTRAL_PASS : getenv('KIW_CENTRAL_PASS');
        
        // Falls keine .env vorhanden ist, wird hier abgebrochen, um unsichere Calls zu verhindern
        if (!$auth_user || !$auth_pass) {
            return false;
        }

        $payload = [
            'target'    => $target_url,
            'method'    => $args['method'] ?? 'GET',
            'body'      => $args['body'] ?? [],
            'module_id' => get_option('kiw_module_id')
        ];

        $response = wp_remote_post(self::$zentrale_url, [
            'timeout' => 15,
            'headers' => [
                'Content-Type'  => 'application/json',
                'Authorization' => 'Basic ' . base64_encode("$auth_user:$auth_pass")
            ],
            'body' => json_encode($payload)
        ]);

        // Fehlerbehandlung: Wenn WP_Error oder kein JSON zurückkommt
        if (is_wp_error($response)) {
            return false;
        }

        $body = wp_remote_retrieve_body($response);
        return json_decode($body, true);
    }
}