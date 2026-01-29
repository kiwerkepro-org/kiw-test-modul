<?php
/**
 * View for {{MODULE_NAME}}
 * 
 * Brand Guide V1.1 (Dark Mode)
 */
defined('ABSPATH') || exit;
?>

<div class="wrap serenity-dashboard px-4 py-8 bg-[#0A0F1A]">
    <div class="bg-[#111827] rounded-2xl p-8 shadow-sm border border-[#1F2937] hover:border-[#374151] transition-colors relative overflow-hidden group">
        <!-- Glow Effect -->
        <div class="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
            <div class="w-32 h-32 bg-[#00E0B8] blur-[80px] rounded-full"></div>
        </div>

        <h2 class="text-2xl font-bold text-white mb-4 relative z-10">
            <?php echo esc_html__('{{MODULE_NAME}}', '{{MODULE_SLUG}}'); ?>
        </h2>
        
        <p class="text-slate-400 relative z-10">
            <?php echo esc_html__('Dies ist ein Platzhalter für ein neues Modul.', '{{MODULE_SLUG}}'); ?>
        </p>

        <div class="mt-6 flex gap-3 relative z-10">
            <button class="bg-[#00E0B8] text-[#0A0F1A] px-4 py-2 rounded-lg text-sm font-bold shadow-[0_0_20px_rgba(0,224,184,0.15)] hover:brightness-110 transition-all">
                Action
            </button>
            <button class="border border-[#1F2937] text-slate-300 px-4 py-2 rounded-lg text-sm font-medium hover:text-white hover:border-slate-500 transition-all">
                Secondary
            </button>
        </div>
    </div>
</div>
