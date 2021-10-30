# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import time

class CPUsage(object):
    """
    Credits: https://github.com/ebruck/indicator-doom-cpu
    Original: http://www.boduch.ca/2009/02/python-cpu-usage.html
    Forked and modified to work with flatpak by hezral@gmail.com
    """
    def __init__(self, interval=0.1, percentage=True, **kwargs):
        super().__init__(**kwargs)
        self.interval = interval
        self.percentage = percentage
        self.result = self.compute()

    def get_time(self):
        stat_file_line0 = self.read_stat_file()
        time_list = stat_file_line0.split(' ')[2:6]
        for i in range(len(time_list)):
            time_list[i] = int(time_list[i])
        return time_list

    def delta_time(self):
        x = self.get_time()
        time.sleep(self.interval)
        y = self.get_time()
        for i in range(len(x)):
            y[i] -= x[i]
        return y

    def compute(self):
        t = self.delta_time()
        if self.percentage:
            result = 100-(t[len(t)-1]*100.00/sum(t))
        else:
            result = sum(t)
        return result

    def __repr__(self):
        return str(self.result)

    @staticmethod
    def read_stat_file():
        """
        Function to copy files to clipboard
        """
        from subprocess import Popen, PIPE

        try:
            run_executable = Popen(['cat', '/proc/stat'], stdout=PIPE)
            stdout, stderr = run_executable.communicate()
            return stdout.splitlines()[0].decode("utf-8")
        except:
            import traceback
            print(traceback.format_exc())