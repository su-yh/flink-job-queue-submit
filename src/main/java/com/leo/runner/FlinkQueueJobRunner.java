package com.leo.runner;

import com.leo.config.properties.BaseProperties;
import com.leo.config.properties.JobProperties;
import com.leo.constants.enums.JobStatus;
import com.leo.util.BizUtils;
import com.leo.util.CdapDateUtils;
import com.leo.util.FlinkJobUtils;
import com.leo.vo.FlinkJobOverviewResultVo;
import com.leo.vo.FlinkJobsOverviewResultVo;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import javax.annotation.PostConstruct;
import java.net.URI;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 * @author suyh
 * @since 2025-03-06
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class FlinkQueueJobRunner implements ApplicationRunner {
    private final BaseProperties properties;
    private final RestTemplate restTemplate;

    private URI uriJobsOverview;

    @PostConstruct
    public void init() {
        initUri();
    }

    private void initUri() {
        String url = String.format("http://%s:%d/jobs/overview",
                properties.getFlinkWebHost(), properties.getFlinkWebPort());
        UriComponentsBuilder builder = UriComponentsBuilder.fromUriString(url);

        this.uriJobsOverview = builder.build().toUri();
    }

    private URI buildUriJobsJobId(String jobId) {
        String url = String.format("http://%s:%d/jobs/{jobId}",
                properties.getFlinkWebHost(), properties.getFlinkWebPort());
        UriComponentsBuilder builder = UriComponentsBuilder.fromUriString(url);

        Map<String, String> pathParams = new HashMap<>();
        pathParams.put("jobId", jobId);
        return builder.buildAndExpand(pathParams).toUri();
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        log.info("FlinkQueueJobRunner start...");

        doRun();

        log.info("FINISHED.");
    }

    private void doRun() {
        String flinkHome = properties.getFlinkHome();
        List<JobProperties> jobs = properties.getJobs();
        Integer datesStart = properties.getDatesStart();
        Integer datesLast = properties.getDatesLast();
        Integer restartJobNumber = properties.getRestartJobNumber();
        String pns = properties.getPns();
        if (pns == null) {
            pns = "";
        }

        restartFlinkCluster(flinkHome);

        int jobSubmitCount = 0;
        int prevRestartFlinkClusterJobCount = 0;

        long betweenDays = CdapDateUtils.betweenDays(datesStart, datesLast);
        for (int i = 0; i <= betweenDays; i++) {
            int dates = CdapDateUtils.plusDays(datesStart, i);

            for (JobProperties job : jobs) {
                if (!job.isEnabled()) {
                    continue;
                }

                log.info("wait flink cluster idle.");
                waitFlinkClusterIdle();

                String command = FlinkJobUtils.buildJobSubmitCommand(job.getJobName(), flinkHome, job.getJarPath(), dates, pns);
                log.info("submit {} job, command: {}", job.getJobName(), command);
                String jobId = FlinkJobUtils.flinkJobSubmit(command);
                log.info("submit {} job finished, dates: {}, jobId: {}", job.getJobName(), dates, jobId);
                if (jobId == null) {
                    return;
                }
                jobSubmitCount++;
                waitJobFinished(jobId);
            }

//            if (jobCohort.isEnabled()) {
//                log.info("wait flink cluster idle.");
//                waitFlinkClusterIdle();
//                String command = FlinkJobUtils.buildCohortJobSubmitCommand(flinkHome, jobCohort.getJarPath(), dates, pns);
//                log.info("submit cohort job, command: {}", command);
//                String jobId = FlinkJobUtils.flinkJobSubmit(command);
//                log.info("submit cohort job finished, dates: {}, jobId: {}", dates, jobId);
//                if (jobId == null) {
//                    return;
//                }
//                jobSubmitCount++;
//                waitJobFinished(jobId);
//            }
//
//            if (jobRealtime.isEnabled()) {
//                log.info("wait flink cluster idle.");
//                waitFlinkClusterIdle();
//                String command = FlinkJobUtils.buildRealtimeJobSubmitCommand(flinkHome, jobRealtime.getJarPath(), dates, pns);
//                log.info("submit realtime job, command: {}", command);
//                String jobId = FlinkJobUtils.flinkJobSubmit(command);
//                log.info("submit realtime job finished, dates: {}, jobId: {}", dates, jobId);
//                if (jobId == null) {
//                    return;
//                }
//                jobSubmitCount++;
//                waitJobFinished(jobId);
//            }
//
//            if (jobRepetition.isEnabled()) {
//                log.info("wait flink cluster idle.");
//                waitFlinkClusterIdle();
//                String command = FlinkJobUtils.buildRepetitionJobSubmitCommand(flinkHome, jobRepetition.getJarPath(), dates, pns);
//                log.info("submit repetition job, command: {}", command);
//                String jobId = FlinkJobUtils.flinkJobSubmit(command);
//                log.info("submit repetition job finished, dates: {}, jobId: {}", dates, jobId);
//                if (jobId == null) {
//                    return;
//                }
//                jobSubmitCount++;
//                waitJobFinished(jobId);
//            }

            if (jobSubmitCount - prevRestartFlinkClusterJobCount >= restartJobNumber) {
                restartFlinkCluster(flinkHome);
                prevRestartFlinkClusterJobCount = jobSubmitCount;
            }
        }
    }

    private void restartFlinkCluster(String flinkHome) {
        try {
            waitFlinkClusterIdle();
        } catch (Exception ignore) {
        }

        boolean flag;
        do {
            BizUtils.sleepIgnoreException(TimeUnit.SECONDS, 5L);
            flag = FlinkJobUtils.flinkClusterRestart(flinkHome);
        } while (!flag);

        // 重启成功，等一会儿，让集群可以正常使用。
        for (int i = 0; i < 10; i++) {
            BizUtils.sleepIgnoreException(TimeUnit.SECONDS, 1L);
        }
    }

    private void waitFlinkClusterIdle() {
        while (true) {
            List<FlinkJobOverviewResultVo> vos = queryJobOverview();
            if (vos != null) {
                boolean idle = flinkClusterIdle(vos);
                if (idle) {
                    break;
                }
            }

            BizUtils.sleepIgnoreException(TimeUnit.SECONDS, 1L);
        }
    }

    private void waitJobFinished(@NonNull String jobId) {
        while (true) {
            BizUtils.sleepIgnoreException(TimeUnit.SECONDS, 1L);

            FlinkJobOverviewResultVo jobOverviewResultVo = queryJobOverview(jobId);
            if (jobOverviewResultVo == null) {
                throw new RuntimeException("jobOverviewResultVo is null");
            }
            boolean flag = flinkJobFinished(jobOverviewResultVo);
            if (flag) {
                log.info("job finished, jobId: {}", jobId);
                BizUtils.sleepIgnoreException(TimeUnit.SECONDS, 1L);
                break;
            }
        }
    }

    private boolean flinkClusterIdle(@NonNull List<FlinkJobOverviewResultVo> vos) {
        for (FlinkJobOverviewResultVo vo : vos) {
            JobStatus state = vo.getState();
            switch (state) {
                case INITIALIZING:
                case CREATED:
                case RUNNING:
                case FAILING:
                case CANCELLING:
                case RESTARTING:
                case SUSPENDED:
                case RECONCILING:
                    return false;
                default:
                    break;
            }
        }

        // 所有作业非活跃，则集群空闲
        return true;
    }

    private boolean flinkJobFinished(FlinkJobOverviewResultVo vo) {
        JobStatus state = vo.getState();
        switch (state) {
            case INITIALIZING:
            case CREATED:
            case RUNNING:
            case RESTARTING:
            case SUSPENDED:
            case RECONCILING:
                return false;
            case FINISHED:
                return true;
            case FAILING:
            case CANCELLING:
            default:
                throw new RuntimeException("job state abnormal: " + state);
        }
    }

    private List<FlinkJobOverviewResultVo> queryJobOverview() {
        final ResponseEntity<FlinkJobsOverviewResultVo> responseEntity = restTemplate.exchange(
                this.uriJobsOverview, HttpMethod.GET, null, FlinkJobsOverviewResultVo.class);

        if (!responseEntity.getStatusCode().is2xxSuccessful()) {
            log.error("response status: {}", responseEntity.getStatusCode());
            return null;
        }

        FlinkJobsOverviewResultVo jobsOverviewResultVo = responseEntity.getBody();
        if (jobsOverviewResultVo == null) {
            log.error("response body, {} is null.", FlinkJobsOverviewResultVo.class.getSimpleName());
            return null;
        }

        return jobsOverviewResultVo.getJobs();
    }

    private FlinkJobOverviewResultVo queryJobOverview(String jobId) {
        URI uriJobId = buildUriJobsJobId(jobId);

        final ResponseEntity<FlinkJobOverviewResultVo> responseEntity = restTemplate.exchange(
                uriJobId, HttpMethod.GET, null, FlinkJobOverviewResultVo.class);

        if (!responseEntity.getStatusCode().is2xxSuccessful()) {
            log.error("response status: {}", responseEntity.getStatusCode());
            return null;
        }

        FlinkJobOverviewResultVo jobVo = responseEntity.getBody();
        if (jobVo == null) {
            log.error("response body, {} is null.", String.class.getSimpleName());
            return null;
        }

        return jobVo;
    }
}
