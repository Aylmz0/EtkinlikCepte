/**
 * WebSocket client skeleton (H2.20).
 *
 * Reconnects with 1/2/4/8 second backoff (§11) and exposes a frame callback.
 * The auth token is passed as a query parameter because browsers cannot set
 * WebSocket headers.
 */
export type RealtimeFrame = { type: string; payload: unknown };

export class RealtimeClient {
  private socket: WebSocket | null = null;
  private attempt = 0;
  private closed = false;
  private timer: ReturnType<typeof setTimeout> | null = null;

  constructor(
    private readonly baseUrl: string,
    private readonly onFrame: (frame: RealtimeFrame) => void
  ) {}

  connect(token: string): void {
    this.closed = false;
    this.open(token);
  }

  private open(token: string): void {
    const url = new URL('/v1/ws', this.baseUrl);
    url.searchParams.set('token', token);
    const socket = new WebSocket(url);
    this.socket = socket;

    socket.onopen = () => {
      this.attempt = 0;
    };
    socket.onmessage = (event) => {
      try {
        this.onFrame(JSON.parse(String(event.data)) as RealtimeFrame);
      } catch {
        // Malformed frames are ignored; the server closes with 4400.
      }
    };
    socket.onclose = () => {
      if (!this.closed) this.scheduleReconnect(token);
    };
  }

  private scheduleReconnect(token: string): void {
    const delay = [1, 2, 4, 8][Math.min(this.attempt, 3)] * 1000;
    this.attempt += 1;
    this.timer = setTimeout(() => this.open(token), delay);
  }

  send(frame: RealtimeFrame): boolean {
    if (this.socket?.readyState !== WebSocket.OPEN) return false;
    this.socket.send(JSON.stringify(frame));
    return true;
  }

  close(): void {
    this.closed = true;
    if (this.timer) clearTimeout(this.timer);
    this.socket?.close();
    this.socket = null;
  }
}
