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
    departments: [];
    owner_id: number;
    create_date: Date;
    lat: string;
    lng: string;
    id: number;
}

export interface IHospitalUpdate {
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

export interface IDepartmentCreate {
    name: string;
    owner_id: number;
    hospital_id: number;
}

export interface IDepartmentUpdate {
    id: number;
    name: string;
}

export interface IDepartment {
    id: number;
    name: string;
}

export interface ISurvey {
    name: string;
    owner_id: number;
    department_id: number;
    create_date: Date;
    questions: {};
}

export interface ISurveyCreate {
    name: string;
    owner_id: number;
    department_id: number;
    create_date: Date;
    questions: {};
}

export interface IStatistics {
    total_submissions: number;
    by_question: [{
        question: string,
        answer_true_perc: number,
        answer_false_perc: number,
    }];
}
