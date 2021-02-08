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
    departmentSurveys: (state: AdminState) => state.departmentSurveys,
    survey : (state: AdminState) => {
        return { ...state.departmentSurveys }
    },
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