import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AdminState } from './state';

const defaultState: AdminState = {
  users: [],
  moduleNames: [],
  overAllStatistics: [],
  hospitalStatistics: [],
  hospitals: [],
  hospitalDepartments: [],
  departmentSurveys: [],
  byLabReport: [],
  byLabReportAccumulative: [],
  labSubmissionNumbers: [],
};

export const adminModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
