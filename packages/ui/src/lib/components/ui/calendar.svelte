<!--
  @component Calendar
  @desc Self-themed single-date picker popover content (month grid + nav).
    Built to replace the native <input type="date"> popover, which cannot be
    restyled and always follows the OS/browser locale instead of the app's.
  Props:
    - value: string | undefined ($bindable) — selected date as "YYYY-MM-DD", or undefined
    - locale: string — BCP-47 locale for month/weekday names via Intl (e.g. "tr-TR", "en-US")
    - todayLabel: string — label for the "jump to today" action
    - clearLabel: string — label for the "clear selection" action
  Events:
    - onClose: () => void — called after a day is picked or the selection is cleared
-->
<script lang="ts">
  import { ChevronLeft, ChevronRight } from '@lucide/svelte';

  let {
    value = $bindable(),
    locale = 'en-US',
    todayLabel = 'Today',
    clearLabel = 'Clear',
    onClose,
  }: {
    value?: string;
    locale?: string;
    todayLabel?: string;
    clearLabel?: string;
    onClose?: () => void;
  } = $props();

  function toIso(d: Date): string {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }

  const initial = value ? new Date(value + 'T00:00:00') : new Date();
  let viewYear = $state(initial.getFullYear());
  let viewMonth = $state(initial.getMonth());

  const todayIso = toIso(new Date());

  // Monday-first weekday abbreviations, generated from the real calendar so
  // they follow `locale` instead of a hardcoded language.
  const weekdayLabels = Array.from({ length: 7 }, (_, i) =>
    new Intl.DateTimeFormat(locale, { weekday: 'short' }).format(new Date(2023, 0, 2 + i)),
  );

  let monthLabel = $derived(
    new Intl.DateTimeFormat(locale, { month: 'long', year: 'numeric' }).format(
      new Date(viewYear, viewMonth, 1),
    ),
  );

  let weeks = $derived.by(() => {
    const firstOfMonth = new Date(viewYear, viewMonth, 1);
    // getDay(): 0=Sun..6=Sat → shift so Monday is column 0.
    const leadingBlanks = (firstOfMonth.getDay() + 6) % 7;
    const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();

    const cells: { date: Date; inMonth: boolean }[] = [];
    for (let i = leadingBlanks; i > 0; i--) {
      cells.push({ date: new Date(viewYear, viewMonth, 1 - i), inMonth: false });
    }
    for (let day = 1; day <= daysInMonth; day++) {
      cells.push({ date: new Date(viewYear, viewMonth, day), inMonth: true });
    }
    while (cells.length % 7 !== 0 || cells.length < 42) {
      const last = cells[cells.length - 1].date;
      cells.push({
        date: new Date(last.getFullYear(), last.getMonth(), last.getDate() + 1),
        inMonth: false,
      });
    }

    const rows: { date: Date; inMonth: boolean }[][] = [];
    for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));
    return rows;
  });

  function changeMonth(delta: number) {
    const next = new Date(viewYear, viewMonth + delta, 1);
    viewYear = next.getFullYear();
    viewMonth = next.getMonth();
  }

  function pick(date: Date) {
    value = toIso(date);
    onClose?.();
  }

  function jumpToday() {
    const now = new Date();
    viewYear = now.getFullYear();
    viewMonth = now.getMonth();
    pick(now);
  }

  function clear() {
    value = undefined;
    onClose?.();
  }
</script>

<div class="w-72 rounded-2xl bg-white dark:bg-card border border-border/80 shadow-lg p-4 space-y-3">
  <div class="flex items-center justify-between">
    <span class="text-sm font-bold text-foreground capitalize">{monthLabel}</span>
    <div class="flex items-center gap-1">
      <button
        type="button"
        aria-label="Previous month"
        onclick={() => changeMonth(-1)}
        class="w-7 h-7 rounded-full flex items-center justify-center text-muted-foreground hover:bg-muted/60 transition-colors cursor-pointer"
      >
        <ChevronLeft class="w-4 h-4" />
      </button>
      <button
        type="button"
        aria-label="Next month"
        onclick={() => changeMonth(1)}
        class="w-7 h-7 rounded-full flex items-center justify-center text-muted-foreground hover:bg-muted/60 transition-colors cursor-pointer"
      >
        <ChevronRight class="w-4 h-4" />
      </button>
    </div>
  </div>

  <table class="w-full text-center border-collapse">
    <thead>
      <tr>
        {#each weekdayLabels as label}
          <th class="text-[10px] font-semibold text-muted-foreground uppercase pb-1.5">{label}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each weeks as week}
        <tr>
          {#each week as cell}
            {@const iso = toIso(cell.date)}
            {@const isSelected = value === iso}
            {@const isToday = todayIso === iso}
            <td class="p-0.5">
              <button
                type="button"
                onclick={() => pick(cell.date)}
                class="w-8 h-8 rounded-xl text-xs font-medium transition-colors cursor-pointer {isSelected
                  ? 'bg-[#ea580c] text-white font-bold'
                  : cell.inMonth
                    ? 'text-foreground hover:bg-muted/60'
                    : 'text-muted-foreground/40 hover:bg-muted/40'} {isToday && !isSelected
                  ? 'ring-1 ring-[#ea580c]/60'
                  : ''}"
              >
                {cell.date.getDate()}
              </button>
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>

  <div class="flex items-center justify-between pt-1 border-t border-border/60">
    <button
      type="button"
      onclick={clear}
      class="text-xs font-semibold text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
    >
      {clearLabel}
    </button>
    <button
      type="button"
      onclick={jumpToday}
      class="text-xs font-semibold text-[#ea580c] hover:underline cursor-pointer"
    >
      {todayLabel}
    </button>
  </div>
</div>
