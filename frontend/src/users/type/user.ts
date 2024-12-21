export interface User {
    id: string
    email: string
    firstName: string
    lastName: string
    role: string
    emailVerified: boolean
    createdAt: string
    updatedAt: string
}

export interface Profile {
    profileAvatar: string
}
