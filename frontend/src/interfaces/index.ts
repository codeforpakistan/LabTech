export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
    allowed_hospitals?: [];
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    allowed_hospitals?: [];
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    allowed_hospitals?: [];
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
    hospital_type: string;
}

export interface IHospitalUpdate {
    name: string;
    address: string;
    create_date: Date;
    lat: string;
    lng: string;
    id: number;
    hospital_type: string;
}

export interface IHospitalCreate {
    name: string;
    address: string;
    owner_id: number;
    create_date: Date;
    lat: string;
    lng: string;
    hospital_type: string;
}

export interface IDepartmentCreate {
    module_name: string;
    name: string;
    owner_id: number;
    hospital_id: number;
}

export interface IDepartmentUpdate {
    id: number;
    name: string;
    module_name: string;
}

export interface IDepartment {
    id: number;
    name: string;
    module_name: string;
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

export interface ISurveyUpdate {
    id: number;
    name: string;
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
