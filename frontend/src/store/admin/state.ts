import { IUserProfile, IHospital, IDepartment, ISurvey} from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    overAllStatistics: any;
    hospitalStatistics: any;
    hospitals: IHospital[];
    hospitalDepartments: IDepartment[];
    departmentSurveys: ISurvey[];
}
