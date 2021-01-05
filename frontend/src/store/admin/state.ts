import { IUserProfile, IHospital, IDepartment, ISurvey} from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    hospitals: IHospital[];
    hospitalDepartments: IDepartment[];
    departmentSurveys: ISurvey[];
}
