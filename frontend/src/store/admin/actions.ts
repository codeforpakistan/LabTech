import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IHospitalUpdate, ISurveyCreate, IDepartmentCreate, IDepartmentUpdate} from '@/interfaces';
import { IUserProfileCreate, IUserProfileUpdate, IHospitalCreate } from '@/interfaces';
import { State } from '../state';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetUsers, commitSetUser, commitOverAllStatistics, commitHospitalStatistics } from './mutations';
import {  commitSetHospital} from './mutations';
import { commitSetHospitals, commitSetHospitalDepartments, commitSetSurveys} from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';

type MainContext = ActionContext<AdminState, State>;

export const actions = {
    async actionGetHospitals(context: MainContext) {
        try {
            const response = await api.getHospitals(context.rootState.main.token);
            if (response) {
               await commitSetHospitals(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateHospital(context: MainContext, payload: IHospitalCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createHospital(context.rootState.main.token, payload),
                await new Promise<void>((resolve) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetHospital(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Hospital Record created successfully', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetHospitalDepartments(context: MainContext, hospitalId: number) {
        try {
            const response = await api.getHospitalDepartments(context.rootState.main.token, hospitalId);
            if (response) {
                commitSetHospitalDepartments(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateHospital(context: MainContext, payload: { id: number, hospital: IHospitalUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateHospital(context.rootState.main.token, payload.id, payload.hospital),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            // commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Hospital successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetUsers(context: MainContext) {
        try {
            const response = await api.getUsers(context.rootState.main.token);
            if (response) {
                commitSetUsers(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUser(context: MainContext, payload: { id: number, user: IUserProfileUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateUser(context.rootState.main.token, payload.id, payload.user),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createUser(context.rootState.main.token, payload),
                await new Promise((resolve) => setTimeout(() => resolve(payload), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetStatistics(context: MainContext) {
        try {
            const response = await api.getStatistics(context.rootState.main.token);
            if (response) {
                commitOverAllStatistics(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetHospitalStatistics(context: MainContext, ids: any) {
        try {
            const response = await api.getHospitalStatistics(context.rootState.main.token,
            ids.hospitalId, ids.departmentId);
            if (response) {
                commitHospitalStatistics(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateHospitalDepartment(context: MainContext, payload: IDepartmentCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            (await Promise.all([
                api.createHospitalDepartment(context.rootState.main.token, payload),
                await new Promise<void>((resolve) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Department successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateDepartment(context: MainContext, payload: { id: number, department: IDepartmentUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            (await Promise.all([
                api.updateDepartment(context.rootState.main.token, payload.id, payload.department),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Department successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetDepartmentSurveys(context: MainContext, departmentId: number) {
        try {
            const response = await api.getDepartmentSurveys(context.rootState.main.token, departmentId);
            if (response) {
                commitSetSurveys(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetDepartmentSurvey(context: MainContext, surveyId: number) {
        try {
            const response = await api.getSuveyById(context.rootState.main.token, surveyId);
            if (response) {
                commitSetSurveys(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateDepartmentSurvey(context: MainContext, payload: ISurveyCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.CreateDepartmentSurvey(context.rootState.main.token, payload),
                await new Promise<void>((resolve) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Department Survey successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<AdminState, State>('');

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchGetOverAllStatistics = dispatch(actions.actionGetStatistics);
export const dispatchGetHospitalStatistics = dispatch(actions.actionGetHospitalStatistics);

export const dispatchGetHospitals = dispatch(actions.actionGetHospitals);
export const dispatchCreateHospital = dispatch(actions.actionCreateHospital);
export const dispatchUpdateHospital = dispatch(actions.actionUpdateHospital);

export const dispatchGetHospitalDepartments = dispatch(actions.actionGetHospitalDepartments);
export const dispatchCreateHospitalDepartment = dispatch(actions.actionCreateHospitalDepartment);
export const dispatchUpdateDepartment = dispatch(actions.actionUpdateDepartment);

export const dispatchGetDepartmentSurveys = dispatch(actions.actionGetDepartmentSurveys);
export const dispatchCreateDepartmentSurvey = dispatch(actions.actionCreateDepartmentSurvey);
export const dispatchGetDepartmentSurvey = dispatch(actions.actionGetDepartmentSurvey);

