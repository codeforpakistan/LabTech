export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IHospital {
    name: string;
    address: string;
    owner_id: number;
    create_date: Date;
    lat: string;
    lng: string;
    id: number;
}

export interface IHospitalCreate {
    name: string;
    address: string;
    owner_id: number;
    create_date: Date;
    lat: string;
    lng: string;
}
