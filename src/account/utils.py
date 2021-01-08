import math
import time
import random


class PushID:
    # Modeled after base64 web-safe chars, but ordered by ASCII.
    PUSH_CHARS = "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"

    # Lengths of resulting UID and it's parts
    UID_CHARS = 20

    UID_TIMESTAMP_CHARS = 8
    UID_RANDOM_CHARS = UID_CHARS - UID_TIMESTAMP_CHARS

    # Shortcut
    _push_chars_len = len(PUSH_CHARS)

    # Timestamp of last push, used to prevent local collisions if you
    # push multiple times in one ms.
    _last_push_time = 0

    # We generate 72-bits of randomness which get turned into 12
    # characters and appended to the timestamp to prevent
    # collisions with other clients.  We store the last characters
    # we generated because in the event of a collision, we'll use
    # those same characters except "incremented" by one.
    _last_rand_chars = [0] * UID_RANDOM_CHARS

    @classmethod
    def next_id(cls):
        now = math.floor(time.time() * 1000)
        same_millisecond = now == cls._last_push_time

        cls._last_push_time = now

        timestamp_chars = [0] * cls.UID_TIMESTAMP_CHARS

        for i in reversed(range(cls.UID_TIMESTAMP_CHARS)):
            timestamp_chars[i] = cls.PUSH_CHARS[now % cls._push_chars_len]
            now = math.floor(now / cls._push_chars_len)

        assert now == 0, "We should have converted the entire timestamp"

        uid = "".join(timestamp_chars)

        if same_millisecond:
            # If the timestamp hasn't changed since last push, use the
            # same random number, except we increment it.
            for i in reversed(range(cls.UID_RANDOM_CHARS)):
                if cls._last_rand_chars[i] == cls._push_chars_len - 1:
                    cls._last_rand_chars[i] = 0
                else:
                    break

            cls._last_rand_chars[i] += 1
        else:
            for i in range(cls.UID_RANDOM_CHARS):
                cls._last_rand_chars[i] = random.randint(0, cls._push_chars_len - 1)

        for i in range(cls.UID_RANDOM_CHARS):
            uid += cls.PUSH_CHARS[cls._last_rand_chars[i]]

        assert (
            len(uid) == cls.UID_CHARS
        ), f"UID length should be {0}, got {1}: {3}".format(
            cls.UID_CHARS, len(uid), uid
        )

        return uid
