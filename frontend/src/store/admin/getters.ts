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
    adminHospital: (state: AdminState) => state.hospitals,
    adminOneHospital: (state: AdminState) => (userId: number) => {
        const filteredHospitals = state.hospitals.filter((user) => user.id === userId);
        if (filteredHospitals.length > 0) {
            return { ...filteredHospitals[0] };
        }
    },
    hospitalDepartments: (state: AdminState) => state.hospitalDepartments,
    departmentSurveys: (state: AdminState) => state.departmentSurveys,
};

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminUsers = read(getters.adminUsers);
export const readAdminOneHospital = read(getters.adminOneHospital);
export const readAdminHospital = read(getters.adminHospital);
export const readHospitalDepartments = read(getters.hospitalDepartments);
export const readDepartmentSurveys = read(getters.departmentSurveys);


