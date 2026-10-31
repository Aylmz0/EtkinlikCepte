/** Stable TanStack query keys for realtime-driven screens (H2.20). */
export const queryKeys = {
  channels: ['channels'] as const,
  messages: (channelId: string) => ['channels', channelId, 'messages'] as const,
  notifications: ['notifications'] as const
};
