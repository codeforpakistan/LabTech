import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    adminUsers: (state: AdminState) => state.users,
    adminOneUser: (state: AdminState) => (userId: number) => {
        const filteredUsers = state.users.filter((user) => user.id === userId);
        if (filteredUsers.length > 0) {
            return { ...filteredUsers[0] };
        }
    },
    overAllStatistics: (state: AdminState) => state.overAllStatistics,
    readHospitalsStatistics: (state: AdminState) => state.hospitalStatistics,
    adminHospital: (state: AdminState) => state.hospitals,
    adminOneHospital: (state: AdminState) => (userId: number) => {
        const filteredHospitals = state.hospitals.filter((user) => user.id === userId);
        if (filteredHospitals.length > 0) {
            return { ...filteredHospitals[0] };
        }
    },
    adminOneDepartment: (state: AdminState) => (departmentId: number) => {
        const filteredDepartments =
            state.hospitalDepartments.filter((department) => department && department.id === departmentId);
        if (filteredDepartments.length > 0) {
            return { ...filteredDepartments[0] };
        }
    },
    hospitalDepartments: (state: AdminState) => state.hospitalDepartments,
    moduleNames: (state: AdminState) => state.moduleNames,
    departmentSurveys: (state: AdminState) => state.departmentSurveys,
    survey : (state: AdminState) => {
        return { ...state.departmentSurveys };
    },
    byLabReport: (state: AdminState) => state.byLabReport,
    byLabReportAccumulative: (state: AdminState) => {
        console.log('state.byLabReportAccumulative', state.byLabReportAccumulative);
        if (state.byLabReportAccumulative) {
            let list: any = [];
            Object.keys(state.byLabReportAccumulative).forEach(key => {
                let data = state.byLabReportAccumulative[key];
                let indicators = data.indicators.map((x) => { 
                    return { Indicator: x.indicator_name, Score: x.score.toFixed(2) }
                });
                data.indicators = indicators;
                list.push({name: key, data: state.byLabReportAccumulative[key]}) ;
            });
            return list;
        }
        return [];
    },
    labSubmissionNumbers: (state: AdminState) => state.labSubmissionNumbers,
};

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminUsers = read(getters.adminUsers);

export const readHospitalsStatistics = read(getters.readHospitalsStatistics);
export const readAdminOneHospital = read(getters.adminOneHospital);
export const readAdminHospital = read(getters.adminHospital);

export const readOverAllStatistics = read(getters.overAllStatistics);

export const readHospitalDepartments = read(getters.hospitalDepartments);
export const readDepartmentSurveys = read(getters.departmentSurveys);
export const readSurveyById = read(getters.survey);
export const readAdminOneDepartment = read(getters.adminOneDepartment);
export const readByLabReport = read(getters.byLabReport);
export const readbyLabReportAccumulative = read(getters.byLabReportAccumulative);
export const readlabSubmissionNumbers = read(getters.labSubmissionNumbers);
export const readModuleNames = read(getters.moduleNames);
