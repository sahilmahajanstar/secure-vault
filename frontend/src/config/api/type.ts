export interface ServerUser {
    id: string
    email: string
    first_name: string
    last_name: string
    email_verified: boolean
    created_at: string
    updated_at: string
    role: string
}

export interface ServerProfile {
    profile_avatar: string
}

export interface ServerFile {
    id: string
    name: string
    size: number
    user_id: string
    file_url: string
    is_favorite: boolean
    share_type: string
    is_deleted: boolean
    created_at: string
    updated_at: string
    file_metadata: ServerFileMetadata
    user_file_share_info: ServerFileShare
    user: ServerUser
}

export interface ServerFileMetadata {
    id: string
    type: string
    is_folder: boolean
    content_type: string
    created_at: string
    updated_at: string
    size: number
    file_id: string
}

export interface ServerFilePermission {
    id: string
    name: string
    share_file_id: string
}

export interface ServerFileShare {
    id: string
    file_id: string
    user_id: string
    permissions: ServerFilePermission[]
}

export interface ServerFileShareLink {
    id: string
    file_id: string
    user_id: string
    expires_at: string
}
