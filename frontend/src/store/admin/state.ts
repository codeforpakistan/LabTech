import { IUserProfile } from '@/interfaces';
import { IHospital } from '@/interfaces';


export interface AdminState {
    users: IUserProfile[];
    hospitals: IHospital[];
}
