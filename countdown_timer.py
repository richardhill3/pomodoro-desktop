class CountdownTimer:
    def __init__(self, label_var, root, duration_minutes=1):
        self.label_var = label_var
        self.root = root
        self.remaining_seconds = duration_minutes * 60
        self.running = False
        self._job = None

    def start(self):
        if not self.running:
            self.running = True
            self._countdown()

    def reset(self, minutes):
        self.stop()
        self.remaining_seconds = minutes * 60
        self._update_label()

    def stop(self):
        self.running = False
        if self._job:
            self.root.after_cancel(self._job)
            self._job = None

    def _countdown(self):
        if self.remaining_seconds <= 0:
            self.running = False
            self.root.event_generate("<<TimerDone>>")
            return
        if self.remaining_seconds % 60 == 0:
            self.root.event_generate("<<TimerMinuteTick>>")

        self.root.event_generate("<<TimerTick>>")
        self._update_label()
        self.remaining_seconds -= 1
        self._job = self.root.after(1000, self._countdown)

    def _update_label(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.label_var.set(f"{minutes:02}:{seconds:02}")
