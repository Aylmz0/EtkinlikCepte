/**
 * Shared mock conversation list used by Mesajlar and the chat thread screen
 * until the real messaging API lands (§1.6). Reactive ($state) so a chat
 * started on /messages/new shows up immediately and /channels/[id] can look
 * up who it's with.
 */

export interface ChatMessage {
  id: number;
  mine: boolean;
  text: string;
  time: string;
}

export interface Conversation {
  id: string;
  name: string;
  lastMessage: string;
  time: string;
  unread: number;
  online: boolean;
  thread: ChatMessage[];
}

export const conversations = $state<Conversation[]>([
  {
    id: '1',
    name: 'Kullanıcı adı',
    lastMessage: 'Selam, biletini aldın mı?',
    time: '14:22',
    unread: 2,
    online: true,
    thread: [
      { id: 1, mine: false, text: 'Selam, biletini aldın mı?', time: '14:20' },
      { id: 2, mine: true, text: 'Az önce aldım, görüşürüz!', time: '14:22' },
    ],
  },
  {
    id: '2',
    name: 'Kullanıcı adı',
    lastMessage: 'Yarınki provaya geliyor musun?',
    time: '09:10',
    unread: 0,
    online: false,
    thread: [],
  },
  {
    id: '3',
    name: 'Kullanıcı adı',
    lastMessage: 'Fotoğrafları gönderdim, bakabilir misin?',
    time: 'Dün',
    unread: 0,
    online: true,
    thread: [],
  },
  {
    id: '4',
    name: 'Kullanıcı adı',
    lastMessage: 'Teşekkürler, görüşmek üzere!',
    time: 'Pzt',
    unread: 0,
    online: false,
    thread: [],
  },
  {
    id: '5',
    name: 'Kullanıcı adı',
    lastMessage: 'Kulüp sohbetine davet ettim.',
    time: '06.11',
    unread: 5,
    online: false,
    thread: [],
  },
]);

function slugify(name: string): string {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

/**
 * Starts a new conversation with the given contact name (frontend-only —
 * not sent to a backend). Returns the created conversation so the caller
 * can navigate to its chat thread.
 *
 * @param name Display name of the person to chat with.
 */
export function addConversation(name: string): Conversation {
  const base = slugify(name) || 'sohbet';
  let id = base;
  let suffix = 1;
  while (conversations.some((c) => c.id === id)) {
    id = `${base}-${++suffix}`;
  }
  const created: Conversation = {
    id,
    name,
    lastMessage: '',
    time: '',
    unread: 0,
    online: false,
    thread: [],
  };
  conversations.push(created);
  return created;
}

/**
 * Removes a conversation from the shared catalogue (frontend-only — not
 * sent to a backend).
 *
 * @param id Conversation id to remove.
 */
export function removeConversation(id: string): void {
  const index = conversations.findIndex((c) => c.id === id);
  if (index !== -1) conversations.splice(index, 1);
}

/**
 * Returns the existing conversation with this contact name, or starts a new
 * one — used when messaging someone from outside Mesajlar (e.g. "Mesaj
 * Gönder" on an event's page) so repeat visits reuse the same thread instead
 * of spawning a new one each time.
 *
 * @param name Display name of the person to chat with.
 */
export function findOrCreateConversation(name: string): Conversation {
  const existing = conversations.find(
    (c) => c.name.toLocaleLowerCase('tr') === name.toLocaleLowerCase('tr'),
  );
  return existing ?? addConversation(name);
}
