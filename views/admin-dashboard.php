<?php
/**
 * Admin Dashboard View for Serenity WP (Dark Mode V1.1)
 * 
 * Brand Guide V1.1 Compliance:
 * - Background: #0A0F1A
 * - Cards: #111827
 * - Accent: #00E0B8
 * - Typography: Inter
 */

defined('ABSPATH') || exit;

/**
 * Logic Section: Prepare data for the dashboard.
 */
function kiw_get_dashboard_data() {
    return [
        'meta' => [
            'page_title'    => esc_html__('Test Modul', 'kiw-test-modul'),
            'welcome_msg'   => esc_html__('Willkommen zurück bei Test Modul.', 'kiw-test-modul'),
            'doc_label'     => esc_html__('Dokumentation', 'kiw-test-modul'),
            'new_mod_label' => esc_html__('Neues Modul', 'kiw-test-modul'),
        ],
        'stats' => [
            'performance' => '98.2%',
            'efficiency'  => [
                'label' => esc_html__('System Efficiency', 'kiw-test-modul'),
                'value' => '+12.5%',
            ],
            'tasks' => [
                'label' => esc_html__('Active Tasks', 'kiw-test-modul'),
                'count' => 24,
            ],
            'errors' => [
                'label' => esc_html__('System Health', 'kiw-test-modul'),
                'count' => '100%',
                'status' => 'Optimal'
            ],
        ],
        'premium' => [
            'title'       => esc_html__('Test Modul ELITE', 'kiw-test-modul'),
            'description' => esc_html__('Aktiviere die KI-Engine für maximale Performance.', 'kiw-test-modul'),
            'cta'         => esc_html__('Upgrade', 'kiw-test-modul'),
            'badge'       => 'PRO',
        ],
        'quick_actions' => [
            [
                'title'       => esc_html__('Global Settings', 'kiw-test-modul'),
                'description' => esc_html__('Konfiguration & API Keys', 'kiw-test-modul'),
                'icon'        => 'settings',
                'bg_color'    => 'bg-gray-800',
                'icon_color'  => 'text-brand-accent',
                'hover_bg'    => 'group-hover:bg-gray-700',
            ],
            [
                'title'       => esc_html__('Live Updates', 'kiw-test-modul'),
                'description' => esc_html__('System ist aktuell', 'kiw-test-modul'),
                'icon'        => 'zap',
                'bg_color'    => 'bg-gray-800',
                'icon_color'  => 'text-green-400',
                'hover_bg'    => 'group-hover:bg-gray-700',
            ],
        ],
        'footer' => [
            'version' => defined('KIW_TEST_MODUL_VERSION') ? KIW_TEST_MODUL_VERSION : '0.1.0', // Fallback safety
            'privacy' => esc_html__('Datenschutz', 'kiw-test-modul'),
            'support' => esc_html__('Support', 'kiw-test-modul'),
        ]
    ];
}

// Initialize Logic
$dashboard = kiw_get_dashboard_data();
?>

<!-- Framework & Icon Assets -->
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>

<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    brand: {
                        bg: '#0A0F1A',
                        card: '#111827',
                        border: '#1F2937',
                        accent: '#00E0B8', // Cyan Neon
                    }
                },
                fontFamily: {
                    sans: ['Inter', 'sans-serif'],
                },
                boxShadow: {
                    'neon': '0 0 20px rgba(0, 224, 184, 0.15)',
                }
            }
        }
    }
</script>

<style>
    /* WP Admin Overrides for Immersive Dark Mode */
    #wpcontent, #wpbody-content { background: #0A0F1A !important; padding-left: 0 !important; }
    .wrap { margin: 0 !important; max-width: 100% !important; }
    
    .serenity-dashboard { 
        font-family: 'Inter', system-ui, sans-serif; 
        color: #e2e8f0;
    }
    
    .bento-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        transition: all 0.2s ease-in-out;
    }
    
    .bento-card:hover {
        border-color: #374151;
        transform: translateY(-2px);
    }
    
    .lucide { display: inline-block; vertical-align: middle; }
</style>

<div class="serenity-dashboard p-6 md:p-10 min-h-screen bg-brand-bg">
    
    <!-- Header -->
    <header class="mb-12 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
            <h1 class="text-3xl font-bold text-white tracking-tight !p-0 !m-0 mb-2 uppercase">
                <?php echo $dashboard['meta']['page_title']; ?>
            </h1>
            <p class="text-slate-400 text-base">
                <?php echo $dashboard['meta']['welcome_msg']; ?>
            </p>
        </div>
        <div class="flex items-center gap-3">
            <button class="bg-brand-card border border-brand-border text-slate-300 px-5 py-2.5 rounded-lg text-sm font-medium hover:text-white hover:border-slate-600 transition-all">
                <?php echo $dashboard['meta']['doc_label']; ?>
            </button>
            <button class="bg-brand-accent text-brand-bg px-6 py-2.5 rounded-lg text-sm font-bold shadow-neon hover:brightness-110 transition-all">
                <?php echo $dashboard['meta']['new_mod_label']; ?>
            </button>
        </div>
    </header>

    <!-- Bento Grid -->
    <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        <!-- Large Stats Card (Span 8) -->
        <div class="md:col-span-8 bento-card rounded-2xl p-8 relative overflow-hidden group">
            <div class="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity">
                <i data-lucide="activity" class="text-brand-accent w-32 h-32"></i>
            </div>
            
            <div class="relative z-10">
                <div class="flex items-center gap-3 mb-6">
                    <span class="w-2 h-2 rounded-full bg-brand-accent animate-pulse shadow-neon"></span>
                    <span class="text-xs font-semibold uppercase tracking-wider text-brand-accent">
                        <?php echo esc_html__('System Status', 'kiw-test-modul'); ?>
                    </span>
                </div>
                
                <h2 class="text-5xl font-bold text-white mb-8 tracking-tighter">
                    <?php echo $dashboard['stats']['performance']; ?>
                </h2>
                
                <div class="grid grid-cols-3 gap-8">
                    <div>
                        <p class="text-xs text-slate-500 uppercase font-bold mb-1"><?php echo $dashboard['stats']['efficiency']['label']; ?></p>
                        <p class="text-lg font-medium text-emerald-400"><?php echo $dashboard['stats']['efficiency']['value']; ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-slate-500 uppercase font-bold mb-1"><?php echo $dashboard['stats']['tasks']['label']; ?></p>
                        <p class="text-lg font-medium text-slate-200"><?php echo $dashboard['stats']['tasks']['count']; ?></p>
                    </div>
                    <div>
                        <p class="text-xs text-slate-500 uppercase font-bold mb-1"><?php echo $dashboard['stats']['errors']['label']; ?></p>
                        <p class="text-lg font-medium text-brand-accent"><?php echo $dashboard['stats']['errors']['status']; ?></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Update / Premium Card (Span 4) -->
        <div class="md:col-span-4 bento-card rounded-2xl p-8 bg-gradient-to-b from-brand-card to-gray-900 flex flex-col justify-between relative overflow-hidden">
            <div class="absolute -right-4 -top-4 opacity-10">
                <i data-lucide="zap" class="text-yellow-400 w-24 h-24"></i>
            </div>
            
            <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs font-bold mb-4">
                    <?php echo $dashboard['premium']['badge']; ?>
                </div>
                <h3 class="text-xl font-bold text-white mb-2"><?php echo $dashboard['premium']['title']; ?></h3>
                <p class="text-slate-400 text-sm leading-relaxed mb-6">
                    <?php echo $dashboard['premium']['description']; ?>
                </p>
            </div>
            
            <button class="w-full flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white py-3 rounded-lg font-medium transition-colors">
                <?php echo $dashboard['premium']['cta']; ?>
                <i data-lucide="chevron-right" class="w-4 h-4"></i>
            </button>
        </div>

        <!-- Quick Actions Row -->
        <?php foreach ($dashboard['quick_actions'] as $action): ?>
        <div class="md:col-span-6 bento-card rounded-2xl p-6 group cursor-pointer flex items-center gap-5">
            <div class="w-14 h-14 rounded-xl <?php echo $action['bg_color']; ?> flex items-center justify-center shrink-0 border border-brand-border group-hover:border-brand-accent/30 transition-colors">
                <i data-lucide="<?php echo $action['icon']; ?>" class="<?php echo $action['icon_color']; ?> w-6 h-6"></i>
            </div>
            <div>
                <h4 class="text-base font-bold text-white mb-1 group-hover:text-brand-accent transition-colors"><?php echo $action['title']; ?></h4>
                <p class="text-sm text-slate-400"><?php echo $action['description']; ?></p>
            </div>
            <div class="ml-auto opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0">
                <i data-lucide="arrow-right" class="text-brand-accent w-5 h-5"></i>
            </div>
        </div>
        <?php endforeach; ?>

    </div>

    <!-- Footer -->
    <footer class="mt-16 border-t border-brand-border pt-8 flex flex-col md:flex-row justify-between items-center text-xs text-slate-600 font-medium uppercase tracking-wider">
        <div>
            <?php printf(esc_html__('Test Modul Suite v%s', 'kiw-test-modul'), defined('KIW_TEST_MODUL_VERSION') ? KIW_TEST_MODUL_VERSION : '0.1.0'); ?>
        </div>
        <div class="flex gap-6 mt-4 md:mt-0">
            <a href="#" class="hover:text-brand-accent transition-colors"><?php echo $dashboard['footer']['privacy']; ?></a>
            <a href="#" class="hover:text-brand-accent transition-colors"><?php echo $dashboard['footer']['support']; ?></a>
        </div>
    </footer>
</div>

<script>
    lucide.createIcons();
</script>
