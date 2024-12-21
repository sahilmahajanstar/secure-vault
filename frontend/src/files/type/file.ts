import { User } from '../../users/type/user'

export interface File {
    id: string
    name: string
    userId: string
    size: number
    isFavorite: boolean
    shareType: string
    isDeleted: boolean
    fileMetadata: FileMetadata | null
    user: User | null
    userFileShareInfo: FileShare | null
}

export interface FileMetadata {
    id: string
    type: string
    isFolder: boolean
    contentType: string
    createdAt: string
    updatedAt: string
    size: number
    fileId: string
}

export interface FileShare {
    id: string
    fileId: string
    userId: string
    permissions: FilePermissions[]
}

export interface FilePermissions {
    id: string
    name: string
    shareFileId: string
}

export interface FileShareLink {
    id: string
    fileId: string
    expiresAt: string
    userId: string
}
