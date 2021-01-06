import { IUserProfile } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    overAllStatistics: any;
    hospitalStatistics: any;
}
