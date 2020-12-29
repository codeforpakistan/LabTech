import { IUserProfile, IHospital, IDepartment } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    hospitals: IHospital[];
    departments: IDepartment[];
}
