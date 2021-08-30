import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate,
  IUserProfileCreate, IHospital, IHospitalUpdate, IHospitalCreate,
  IDepartmentCreate, ISurveyCreate, IDepartment, ISurveyUpdate } from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getHospitals(token: string) {
    return axios.get<IHospital[]>(`${apiUrl}/api/v1/hospitals/`, authHeaders(token));
  },
  async createHospital(token: string, data: IHospitalCreate) {
    return axios.post(`${apiUrl}/api/v1/hospitals/?create_indicators=${data.isCreateWithDefault ? 1 : 0}`,
    data, authHeaders(token));
  },
  async updateHospital(token: string, hospitalId: number, data: IHospitalUpdate) {
    return axios.put(`${apiUrl}/api/v1/hospitals/${hospitalId}`, data, authHeaders(token));
  },
  async getHospitalDepartments(token: string, hospitalId: number) {
    return axios.get<IDepartment[]>(`${apiUrl}/api/v1/departments/?hospital_id=` + hospitalId, authHeaders(token));
  },
  async deleteHospital(token: string, hospitalId: number) {
    return axios.delete(`${apiUrl}/api/v1/hospitals/` + hospitalId, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async createHospitalDepartment(token: string, data: IDepartmentCreate) {
    return axios.post(`${apiUrl}/api/v1/departments/`, data, authHeaders(token));
  },
  async updateDepartment(token: string, departmentId: number, data: IDepartment) {
    return axios.put(`${apiUrl}/api/v1/departments/${departmentId}`, data, authHeaders(token));
  },
  async CreateDepartmentSurvey(token: string, data: ISurveyCreate) {
    return axios.post(`${apiUrl}/api/v1/surveys/`, data, authHeaders(token));
  },
  async UpdateDepartmentSurvey(token: string, surveyId: number, data: ISurveyUpdate) {
    return axios.put(`${apiUrl}/api/v1/surveys/${surveyId}`, data, authHeaders(token));
  },
  async getDepartmentSurveys(token: string, departmentId: number) {
    return axios.get(`${apiUrl}/api/v1/surveys/?department_id=` + departmentId, authHeaders(token));
  },
  async getModuleNames(token: string) {
    return axios.get(`${apiUrl}/api/v1/departments/module_names/all`, authHeaders(token));
  },
  async getSuveyById(token: string, surveyId: number) {
    return axios.get(`${apiUrl}/api/v1/surveys/` + surveyId, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getStatistics(token: string) {
    return axios.get(`${apiUrl}/api/v1/submissions/report/by-questions`, authHeaders(token));
  },
  async getHospitalStatistics(token: string, hospitalId?: number, departmentId?: number) {
    return axios.get(`${apiUrl}/api/v1/submissions/report/by-questions/`
    + hospitalId + '/' + (departmentId ? departmentId : 0), authHeaders(token));
  },
  async getByLabReport(token: string) {
    return axios.get(`${apiUrl}/api/v1/submissions/by-labs`, authHeaders(token));
  },
  async byLabAccumulative(token: string, query: string = '') {
    if (!query) {
      query = '?apply_filter=0&lab_id=5&submission_no=0';
    }
    return axios.get(`${apiUrl}/api/v1/submissions/report-by-lab-submission${query}`, authHeaders(token));
  },
  async getLabSubmissions(token: string, labID: string = '5') {
    return axios.get(`${apiUrl}/api/v1/submissions/submission_nos/by-lab?lab_id=${labID}`, authHeaders(token));
  },
};
