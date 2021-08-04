import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AdminState } from './state';

const defaultState: AdminState = {
  users: [],
  overAllStatistics: [],
  hospitalStatistics: [],
  hospitals: [],
  hospitalDepartments: [],
  departmentSurveys: [],
  byLabReport: [],
};

export const adminModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
