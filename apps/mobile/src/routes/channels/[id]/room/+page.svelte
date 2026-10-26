<!--
  @component ChannelRoomPage
  @desc Direct 1-on-1 private live audio/video call room (§1.6, Owner: P5).
    The actual LiveKit connection is backend-dependent and not wired here;
    mic and camera buttons only toggle their own local icon state.
  Props: None
  Events: None
-->
<script lang="ts">
  import { Mic, MicOff, Video, VideoOff, PhoneOff } from '@lucide/svelte';
  import { t } from '$lib/i18n.js';

  let micOn = $state(true);
  let cameraOn = $state(true);
</script>

<div class="min-h-screen bg-[#121214] text-white flex flex-col px-6 py-8 max-w-sm mx-auto">
  <div class="flex-1 flex flex-col items-center justify-center gap-3">
    <div
      class="w-28 h-28 rounded-full bg-[#dcfce7]/20 flex items-center justify-center text-2xl font-bold text-emerald-300"
    >
      KA
    </div>
    <h1 class="text-base font-semibold text-white/90">{t('profile.user_name')}</h1>
    <p class="text-xs text-white/50">{t('room.calling')}</p>
  </div>

  <div class="flex items-center justify-center gap-4 pb-4">
    <button
      type="button"
      onclick={() => (micOn = !micOn)}
      aria-label={t('room.mic')}
      class="w-13 h-13 rounded-full flex items-center justify-center transition-colors cursor-pointer {micOn
        ? 'bg-white/10 text-white hover:bg-white/15'
        : 'bg-white text-[#121214]'}"
    >
      {#if micOn}<Mic class="w-5 h-5" />{:else}<MicOff class="w-5 h-5" />{/if}
    </button>
    <a
      href="../"
      aria-label={t('room.leave')}
      class="w-14 h-14 rounded-full bg-[#ef4444] hover:bg-[#dc2626] flex items-center justify-center transition-colors"
    >
      <PhoneOff class="w-5 h-5" />
    </a>
    <button
      type="button"
      onclick={() => (cameraOn = !cameraOn)}
      aria-label={t('room.camera')}
      class="w-13 h-13 rounded-full flex items-center justify-center transition-colors cursor-pointer {cameraOn
        ? 'bg-white/10 text-white hover:bg-white/15'
        : 'bg-white text-[#121214]'}"
    >
      {#if cameraOn}<Video class="w-5 h-5" />{:else}<VideoOff class="w-5 h-5" />{/if}
    </button>
  </div>
</div>
