<template>
  <md-layout
    class="result"
    md-column
  >
    <md-whiteframe class="statuses-container-frame" md-elevation="2">
      <md-layout class="statuses-container" md-row>
        <result-status
          class="status-container"
          :title="$t('result.status.paper')"
          :status="formattedStatuses.essay.status"
          :instructions="formattedStatuses.essay.instructions"
          md-flex
        />
        <result-status
          class="status-container"
          :title="$t('result.status.networkConstruction')"
          :status="formattedStatuses.construction.status"
          :instructions="formattedStatuses.construction.instructions"
          md-flex
        />
        <result-status
          class="status-container"
          :title="$t('result.status.networkAnalysis')"
          :status="formattedStatuses.analysis.status"
          :instructions="formattedStatuses.analysis.instructions"
          md-flex
        />
      </md-layout>
    </md-whiteframe>
    <md-whiteframe class="time-container">
      <span v-show="!isJobAllDone" class="md-body-1">
        {{ $t('result.time.notDone') }}
      </span>
      <md-layout v-show="isJobAllDone" md-column>
        <span class="md-body-1">
          {{
            $t('result.time.dateFormat', {
              startDisplayDate: displayDate.start,
              endDisplayDate: displayDate.end,
            })
          }}
        </span>
        <span class="md-body-1">
          {{
            $t('result.time.durationFormat', {
              displayHour: displayTime.hour,
              displayMin: displayTime.min,
              displaySec: displayTime.sec,
            })
          }}
        </span>
      </md-layout>
    </md-whiteframe>
    <result-parameter
      class="parameter-container"
      :searchOptions="parameters.searchOptions"
      :coOccurenceOptions="parameters.coOccurenceOptions"
    />
    <router-view
      class="router-container"
      :jobKey="jobKey"
      :jobId="jobId"
      :onSymbolClick="hgncId => handleSymbolClick(hgncId)"
    />
  </md-layout>
</template>

<script>
import _ from 'lodash';
import moment from 'moment';

import Bus from '../../components/Bus';
import ResultStatus from './ResultStatus';
import ResultParameter from './ResultParameter';
import ResultStatusType from '../../structures/ResultStatusType';

import pullingConfig from '../../configs/pulling';

function getEssayStatus(statusObj) {
  if (_.isUndefined(statusObj)) {
    return ResultStatusType.yet;
  }
  const { collect, insert } = statusObj;
  if (_.isUndefined(collect) || _.isUndefined(insert)) {
    return ResultStatusType.yet;
  }
  if (collect === 0) {
    return ResultStatusType.yet;
  }
  if (insert === 5) {
    return ResultStatusType.done;
  }
  return ResultStatusType.running;
}

function getConstructionStatus(wekaCode) {
  if (_.isUndefined(wekaCode)) {
    return ResultStatusType.yet;
  }
  if (wekaCode === 0) {
    return ResultStatusType.yet;
  }
  if (wekaCode === 5) {
    return ResultStatusType.done;
  }
  return ResultStatusType.running;
}

function getAnalysisStatus(networkCode) {
  if (_.isUndefined(networkCode)) {
    return ResultStatusType.yet;
  }
  if (networkCode <= 2) {
    return ResultStatusType.yet;
  }
  if (networkCode === 6) {
    return ResultStatusType.done;
  }
  return ResultStatusType.running;
}

export default {
  name: 'result',
  components: {
    'result-status': ResultStatus,
    'result-parameter': ResultParameter,
  },
  watch: {
    '$route.params'(newParams) {  // eslint-disable-line object-shorthand
      const jobKey = _.get(newParams, 'jobKey');
      this.getJobData(jobKey);
    },
    formattedStatuses(newFormattedStatuses) {
      if (_.get(newFormattedStatuses, 'essay.status') === ResultStatusType.done &&
        _.get(newFormattedStatuses, 'construction.status') === ResultStatusType.done &&
        _.get(newFormattedStatuses, 'analysis.status') === ResultStatusType.done) {
        Bus.$emit('clear-all');
      }
    },
  },
  methods: {
    startGetJobDataTimer() {
      console.log('Firing pull getJobData');  // eslint-disable-line no-console
      const { jobKey } = this.$route.params;
      this.getJobData(jobKey);
      this.getJobDataTimerId = _.delay(
        this.startGetJobDataTimer, pullingConfig.timerMillis);
    },
    getJobData(jobKey) {
      if (_.isUndefined(jobKey)) return;
      this.$http.get(`key2ids/${jobKey}`)
        .then((response) => {
          const jobId = _.get(response.body, '[0].J_ID');
          return this.$http.get(`jobs/${jobId}`);
        })
        .then((response) => {
          const rawJob = _.get(response.body, '[0]');
          this.job = {
            id: rawJob.J_ID,
            key: rawJob.J_KEY,
            query: rawJob.QUERY,
            metricScore: rawJob.MIN_NODE_SUP,
            nodeSize: rawJob.NODE_SIZE,
            isTooSmall: rawJob.TOO_SMALL === 1,
            email: rawJob.EMAIL,
            time: {
              start: rawJob.JOB_START_TIME,
              end: rawJob.JOB_DONE_TIME,
            },
            period: {
              start: rawJob.START_DATE,
              end: rawJob.END_DATE,
            },
            parameters: {
              MIN_SUP: rawJob.MIN_SUP,
              MAX_PVAL: rawJob.MAX_PVAL,
              COOC_EM: rawJob.COOC_EM,
            },
            statuses: {
              essay: {
                status: {
                  collect: rawJob.PMID_COLLECT,
                  insert: rawJob.DO_PMID_INSERT,
                },
                instructions: {
                  pmidCount: rawJob.PMID_COUNT,
                },
              },
              construction: {
                status: rawJob.WEKA,
                instructions: {
                  associationEdgeCount: rawJob.EDGE_NUM_ASSO,
                  coOccurenceEdgeCount: rawJob.EDGE_NUM_COOC,
                  singleOccurNodeCount: rawJob.SINGLE_OCCUR_NODE,
                },
              },
              analysis: {
                status: rawJob.NETWORK,
                instructions: {
                  associationGeneCount: rawJob.GENE_NUM_ASSO,
                  associationNodeTotalCount: rawJob.GENE_NUM_ASSO_NODE,
                  coOccurenceGeneCount: rawJob.GENE_NUM_COOC,
                  coOccurenceNodeTotalCount: rawJob.GENE_NUM_COOC_NODE,
                },
              },
            },
          };
        });
    },
    handleSymbolClick(hgncId) {
      this.$router.push({
        name: 'References',
        params: { hgncId },
      });
    },
  },
  mounted() {
    this.startGetJobDataTimer();
    Bus.$on('clear-all', () => {
      clearTimeout(this.getJobDataTimerId);
    });
  },
  beforeDestroy() {
    clearTimeout(this.getJobDataTimerId);
  },
  data() {
    return {
      job: {},
      getJobDataTimerId: '',
    };
  },
  computed: {
    jobKey() {
      return _.get(this.$route.params, 'jobKey');
    },
    jobId() {
      return this.job.id;
    },
    displayDate() {
      return {
        start: moment(_.get(this.job, 'time.start')).format('YYYY-MM-DD HH:mm:ss'),
        end: moment(_.get(this.job, 'time.end')).format('YYYY-MM-DD HH:mm:ss'),
      };
    },
    displayTime() {
      const startMoment = moment(_.get(this.job, 'time.start'));
      const endMoment = moment(_.get(this.job, 'time.end'));
      const durationMoment = moment.duration(endMoment.diff(startMoment));
      return {
        hour: durationMoment.get('hour'),
        min: durationMoment.get('minute'),
        sec: durationMoment.get('second'),
      };
    },
    formattedStatuses() {
      const essayStatus = {
        status: getEssayStatus(_.get(this.job, 'statuses.essay.status')),
        instructions: [
          {
            id: 0,
            label: this.$t('result.instruction.essay'),
            count: _.get(this.job, 'statuses.essay.instructions.pmidCount'),
          },
        ],
      };
      const constructionStatus = {
        status: getConstructionStatus(
            _.get(this.job, 'statuses.construction.status')),
        instructions: [
          {
            id: 0,
            label: this.$t('result.instruction.construction.coOccurenceEdge'),
            count: _.get(
                this.job,
                'statuses.construction.instructions.coOccurenceEdgeCount'),
          },
          {
            id: 1,
            label: this.$t('result.instruction.construction.singleOccuringNode'),
            count: _.get(
                this.job,
                'statuses.construction.instructions.singleOccurNodeCount'),
          },
        ],
      };
      const analysisStatus = {
        status: getAnalysisStatus(_.get(this.job, 'statuses.analysis.status')),
        instructions: [
          {
            id: 0,
            label: this.$t('result.instruction.analysis.coOccurenceGene'),
            count: _.get(
                this.job,
                'statuses.analysis.instructions.coOccurenceGeneCount'),
          },
          {
            id: 1,
            label: this.$t('result.instruction.analysis.coOccurenceNodeTotal'),
            count: _.get(
                this.job,
                'statuses.analysis.instructions.coOccurenceNodeTotalCount'),
          },
        ],
      };
      return {
        essay: essayStatus,
        construction: constructionStatus,
        analysis: analysisStatus,
      };
    },
    isJobAllDone() {
      return _.get(this.formattedStatuses, 'essay.status') === ResultStatusType.done &&
        _.get(this.formattedStatuses, 'construction.status') === ResultStatusType.done &&
        _.get(this.formattedStatuses, 'analysis.status') === ResultStatusType.done;
    },
    parameters() {
      const toDisplayDate = date => moment(date).format('YYYY-MM-DD');
      const searchOptions = [
        { id: 0,
          label: this.$t('result.parameter.searchOptions.labels.searchQuery'),
          content: _.get(this.job, 'query') },
        { id: 1,
          label: this.$t('result.parameter.searchOptions.labels.searchPeriod'),
          content: `${toDisplayDate(_.get(this.job, 'period.start'))} ~ ${toDisplayDate(_.get(this.job, 'period.end'))}` },
        { id: 2,
          label: this.$t('result.parameter.searchOptions.labels.metricScore'),
          content: _.get(this.job, 'metricScore') },
        { id: 3,
          label: this.$t('result.parameter.searchOptions.labels.singleOccuringNodeSize'),
          content: _.get(this.job, 'nodeSize') },
        { id: 4,
          label: this.$t('result.parameter.searchOptions.labels.userEmail'),
          content: _.get(this.job, 'email') },
      ];
      const convertCoocEM = (coocEMValue) => {
        switch (coocEMValue) {
          case 0:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.support');
          case 1:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.logPvalue');
          case 2:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.oddRatio');
          case 3:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.relativeRisk');
          case 4:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.lift');
          case 5:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.chiSquaredStatistic');
          case 6:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.phiCoefficient');
          case 7:
            return this.$t('result.parameter.coOccurenceOptions.selects.COOC_EM.contingencyCoefficient');
          default:
            return 'ERROR';
        }
      };
      const coOccurenceOptions = [
        { id: 0,
          label: this.$t('result.parameter.coOccurenceOptions.labels.MIN_SUP'),
          content: _.get(this.job, 'parameters.MIN_SUP') },
        { id: 1,
          label: this.$t('result.parameter.coOccurenceOptions.labels.MAX_PVAL'),
          content: _.get(this.job, 'parameters.MAX_PVAL') },
        { id: 2,
          label: this.$t('result.parameter.coOccurenceOptions.labels.COOC_EM'),
          content: convertCoocEM(_.get(this.job, 'parameters.COOC_EM')) },
      ];
      return { searchOptions, coOccurenceOptions };
    },
  },
};
</script>

<style scoped>
.result {
  width: 90%;
  padding: 16px;
  //margin: auto;
}

.statuses-container {
  width: 100%;
}

.statuses-container-frame {
  width: 100%;
  padding: 8px;
  margin: 8px 0;
}

.status-container {
  margin: 8px;
  flex: 1;
}

.time-container {
  width: 100%;
  padding: 16px;
  margin: 8px;
}

.parameter-container {
  width: 100%;
  margin: 8px 0;
}

.router-container {
  width: 100%;
  margin: 8px 0;
}
</style>
