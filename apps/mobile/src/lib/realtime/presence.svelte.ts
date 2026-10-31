/** Presence store fed by `presence.update` frames (H2.20). */
export class PresenceStore {
  online = $state(new Set<string>());

  update(userId: string, status: 'online' | 'offline'): void {
    if (status === 'online') this.online.add(userId);
    else this.online.delete(userId);
    this.online = new Set(this.online);
  }
}

export const presence = new PresenceStore();
