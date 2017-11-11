<template>
  <md-layout
    class="period" md-column md-align="center" md-vertical-align="center"
    md-gutter
  >
    <span class="md-body-2">{{ `Start: ${period.start.format('YYYY/MM/DD')}` }}</span>
    <span class="md-body-2">{{ `End: ${period.end.format('YYYY/MM/DD')}` }}</span>
    <md-button-toggle md-single class="md-primary">
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.all }"
        @click="onUnitClicked(PeriodType.all)"
      >
        {{ $t('period.units.all') }}
      </md-button>
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.lastOneYear }"
        @click="onUnitClicked(PeriodType.lastOneYear)"
      >
        {{ $t('period.units.lastOneYear') }}
      </md-button>
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.lastThreeYears }"
        @click="onUnitClicked(PeriodType.lastThreeYears)"
      >
        {{ $t('period.units.lastThreeYears') }}
      </md-button>
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.lastFiveYears }"
        @click="onUnitClicked(PeriodType.lastFiveYears)"
      >
        {{ $t('period.units.lastFiveYears') }}
      </md-button>
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.lastTenYears }"
        @click="onUnitClicked(PeriodType.lastTenYears)"
      >
        {{ $t('period.units.lastTenYears') }}
      </md-button>
      <md-button
        :class="{ 'md-toggle': periodType === PeriodType.custom }"
        @click="onUnitClicked(PeriodType.custom)"
      >
        {{ $t('period.units.custom') }}
      </md-button>
    </md-button-toggle>
    <div v-show="periodType === PeriodType.custom">
      <span class="md-body-1">Start: </span>
      <datepicker
        v-model="datizedPeriod.start" name="period-start-date-picker"
        :disabled="{
          from: datizedPeriod.end,
          to: moment()
            .set({ year: 1899, month: 11, date: 31 })
            .toDate()
        }"
        @selected="onSelectCustomStartDate"
      />
      <span class="md-body-1">End: </span>
      <datepicker
        v-model="datizedPeriod.end" name="period-end-date-picker"
        :disabled="{
          to: datizedPeriod.start,
        }"
        @selected="onSelectCustomEndDate"
      />
    </div>
  </md-layout>
</template>

<script>
import Vue from 'vue';
import DatePicker from 'vuejs-datepicker';

import moment from 'moment';

import store from '../reducers/Store';

import PeriodType from '../structures/PeriodType';

export default Vue.component('period', {
  components: {
    datepicker: DatePicker,
  },
  mounted() {
    const now = moment();
    store.dispatch(store.actions.setPeriod({
      start: moment().set({ year: 1900, month: 0, date: 1 }),
      end: this.removeTime(now),
    }));
  },
  data() {
    return {
      moment,
      PeriodType,
      periodType: PeriodType.all,
      period: this.$select('period'),
    };
  },
  computed: {
    datizedPeriod() {
      return {
        start: this.period.start.toDate(),
        end: this.period.end.toDate(),
      };
    },
  },
  methods: {
    removeTime(momentObject) {
      return moment().set({
        year: momentObject.get('year'),
        month: momentObject.get('month'),
        date: momentObject.get('date'),
      });
    },
    onUnitClicked(type) {
      this.periodType = type;
      const now = moment();
      switch (type) {
        case PeriodType.all: {
          store.dispatch(store.actions.setPeriod({
            start: moment().set({ year: 1900, month: 0, date: 1 }),
            end: this.removeTime(now),
          }));
          break;
        }
        case PeriodType.lastOneYear: {
          store.dispatch(store.actions.setPeriod({
            start: moment(now).set({ month: 0, date: 1 }),
            end: this.removeTime(now),
          }));
          break;
        }
        case PeriodType.lastThreeYears: {
          store.dispatch(store.actions.setPeriod({
            start: moment(now)
              .subtract(2, 'years')
              .set({ month: 0, date: 1 }),
            end: this.removeTime(now),
          }));
          break;
        }
        case PeriodType.lastFiveYears: {
          store.dispatch(store.actions.setPeriod({
            start: moment(now)
              .subtract(4, 'years')
              .set({ month: 0, date: 1 }),
            end: this.removeTime(now),
          }));
          break;
        }
        case PeriodType.lastTenYears: {
          store.dispatch(store.actions.setPeriod({
            start: moment(now)
              .subtract(9, 'years')
              .set({ month: 0, date: 1 }),
            end: this.removeTime(now),
          }));
          break;
        }
        default:
      }
    },
    onSelectCustomStartDate(newStartDate) {
      store.dispatch(store.actions.setPeriod({
        start: this.removeTime(moment(newStartDate)),
        end: moment(this.datizedPeriod.end),
      }));
    },
    onSelectCustomEndDate(newEndDate) {
      store.dispatch(store.actions.setPeriod({
        start: this.removeTime(moment(this.datizedPeriod.start)),
        end: this.removeTime(moment(newEndDate)),
      }));
    },
  },
});
</script>

<style scoped>
.period {
  margin-bottom: 200px;
}
</style>
