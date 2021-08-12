import { IUserProfile, IHospital, IDepartment, ISurvey, IStatistics} from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    overAllStatistics: any;
    moduleNames: any;
    hospitalStatistics: any;
    hospitals: IHospital[];
    hospitalDepartments: IDepartment[];
    departmentSurveys: ISurvey[];
    byLabReport: any;
}
