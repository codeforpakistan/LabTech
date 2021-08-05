import { IUserProfile, IHospital, IDepartment, ISurvey, IStatistics } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setDepartmentSurveys(state: AdminState, payload: ISurvey[]) {
       state.departmentSurveys = payload;
    },
    setHospitals(state: AdminState, payload: IHospital[]) {
       state.hospitals = payload;
    },
    setHospital(state: AdminState, payload: IHospital) {
        const hospitals = state.hospitals.filter((user: IHospital) => user.id !== payload.id);
        state.hospitals = hospitals;
    },
    setHospitalDepartments(state: AdminState, payload: IDepartment[]) {
        state.hospitalDepartments = payload;
    },
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setAllStatistics(state: AdminState, payload: any[]) {
        state.overAllStatistics = payload;
    },
    setModuleNames(state: AdminState, payload: any[]) {
        state.moduleNames = payload;
    },
    setHospitalStatistics(state: AdminState, payload: any[]) {
        state.hospitalStatistics = payload;
    },
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
export const commitSetHospitals = commit(mutations.setHospitals);
export const commitSetHospital = commit(mutations.setHospital);
export const commitSetHospitalDepartments = commit(mutations.setHospitalDepartments);
export const commitSetSurveys = commit(mutations.setDepartmentSurveys);
export const commitHospitalStatistics = commit(mutations.setHospitalStatistics);
export const commitOverAllStatistics = commit(mutations.setAllStatistics);
export const commitModuleNames = commit(mutations.setModuleNames);

