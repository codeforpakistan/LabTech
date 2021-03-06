import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IHospitalUpdate, ISurveyCreate, IDepartmentCreate, IDepartmentUpdate, ISurveyUpdate} from '@/interfaces';
import { IUserProfileCreate, IUserProfileUpdate, IHospitalCreate } from '@/interfaces';
import { State } from '../state';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetUsers, commitSetUser, commitOverAllStatistics, commitHospitalStatistics, commitModuleNames } from './mutations';
import {  commitSetHospital} from './mutations';
import { commitSetHospitals, commitSetHospitalDepartments, commitSetSurveys, commitByLabReport,
    commitByLabReportAccumulative, commitLabSubmissionNumbers} from './mutations';
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
            const response = await api.createHospital(context.rootState.main.token, payload);
            if (response) {
                commitSetHospital(context, response.data);
                commitRemoveNotification(context, loadingNotification);
                commitAddNotification(context, { content: 'Hospital Record created successfully', color: 'success' });
            }
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
    async actionDeleteHospital(context: MainContext, id: number) {
        try {
            const loadingNotification = { content: 'deleting', showProgress: true };
            const response = await api.deleteHospital(context.rootState.main.token, id);
            if (response) {
                commitRemoveNotification(context, loadingNotification);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetModuleNames(context: MainContext) {
        try {
            const response = await api.getModuleNames(context.rootState.main.token);
            if (response) {
                commitModuleNames(context, response.data);
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
            await api.createHospitalDepartment(context.rootState.main.token, payload);
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
            await api.updateDepartment(context.rootState.main.token, payload.id, payload.department);
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
            await  api.CreateDepartmentSurvey(context.rootState.main.token, payload);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Department Survey successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateDepartmentSurvey(context: MainContext,  payload: { surveyId: number, survey: ISurveyUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            await api.UpdateDepartmentSurvey(context.rootState.main.token, payload.surveyId, payload.survey);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Department Survey successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetByLabReport(context: MainContext) {
        try {
            const response = await api.getByLabReport(context.rootState.main.token);
            if (response) {
                commitByLabReport(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetByLabReportAccumulative(context: MainContext, query: string) {
        try {
            const response = await api.byLabAccumulative(context.rootState.main.token, query);
            if (response) {
                commitByLabReportAccumulative(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetLabSubmissions(context: MainContext, labID: string) {
        try {
            const response = await api.getLabSubmissions(context.rootState.main.token, labID);
            if (response) {
                commitLabSubmissionNumbers(context, response.data);
            }
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
export const dispatchDeleteHospital = dispatch(actions.actionDeleteHospital);

export const dispatchGetHospitalDepartments = dispatch(actions.actionGetHospitalDepartments);
export const dispatchCreateHospitalDepartment = dispatch(actions.actionCreateHospitalDepartment);
export const dispatchUpdateDepartment = dispatch(actions.actionUpdateDepartment);
export const dispatchGetModuleNames = dispatch(actions.actionGetModuleNames);


export const dispatchGetDepartmentSurveys = dispatch(actions.actionGetDepartmentSurveys);
export const dispatchCreateDepartmentSurvey = dispatch(actions.actionCreateDepartmentSurvey);
export const dispatchUpdateDepartmentSurvey = dispatch(actions.actionUpdateDepartmentSurvey);
export const dispatchGetDepartmentSurvey = dispatch(actions.actionGetDepartmentSurvey);
export const dispatchGetByLabReport = dispatch(actions.actionGetByLabReport);
export const dispatchGetByLabReportAccumulative = dispatch(actions.actionGetByLabReportAccumulative);
export const dispatchGetLabSubmissions = dispatch(actions.actionGetLabSubmissions);
