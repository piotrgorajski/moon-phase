from rtc import get_datetime

while True:

    (
        year,
        month,
        day,
        hour,
        minute,
        second
    ) = get_datetime()

    print(
        "%04d-%02d-%02d %02d:%02d:%02d"
        % (
            year,
            month,
            day,
            hour,
            minute,
            second
        )
    )

    import time
    time.sleep(1)