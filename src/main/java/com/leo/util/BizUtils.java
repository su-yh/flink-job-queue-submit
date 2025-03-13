package com.leo.util;

import org.springframework.lang.Nullable;
import org.springframework.util.StringUtils;

import java.util.concurrent.TimeUnit;

/**
 * @author suyh
 * @since 2025-02-20
 */
public class BizUtils {
    public static long parseLongIgnoreException(@Nullable String longValue) {
        if (StringUtils.hasText(longValue)) {
            try {
                return Long.parseLong(longValue);
            } catch (NumberFormatException ignored) {
            }
        }

        return 0L;
    }

    public static void sleepIgnoreException(TimeUnit timeUnit, long timeout) {
        try {
            timeUnit.sleep(timeout);
        } catch (InterruptedException ignored) {
        }
    }
}
