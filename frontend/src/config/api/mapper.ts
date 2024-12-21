import {
    ServerFile,
    ServerFileMetadata,
    ServerFilePermission,
    ServerFileShare,
    ServerFileShareLink,
    ServerProfile,
    ServerUser,
} from './type'

export function mapUser(user: ServerUser) {
    if (!user) {
        return null
    }
    return {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        emailVerified: user.email_verified,
        createdAt: user.created_at,
        updatedAt: user.updated_at,
        role: user.role,
    }
}

export function mapUsers(users: ServerUser[]) {
    return users.map(user => mapUser(user))
}

export function mapProfile(profile: ServerProfile) {
    return {
        profileAvatar: profile.profile_avatar,
    }
}

export function mapFiles(file: ServerFile[]) {
    return file.map(file => mapFile(file))
}

export function mapFile(file: ServerFile) {
    return {
        id: file.id,
        name: file.name,
        createdAt: file.created_at,
        updatedAt: file.updated_at,
        size: file.size,
        isFavorite: file.is_favorite,
        shareType: file.share_type,
        isDeleted: file.is_deleted,
        fileMetadata: mapFileMetadata(file.file_metadata),
        userId: file.user_id,
        user: mapUser(file.user),
        userFileShareInfo: mapFileShare(file.user_file_share_info),
    }
}

export function mapFileMetadata(fileMetadata: ServerFileMetadata) {
    if (!fileMetadata) {
        return null
    }
    return {
        id: fileMetadata.id,
        type: fileMetadata.type,
        isFolder: fileMetadata.is_folder,
        contentType: fileMetadata.content_type,
        createdAt: fileMetadata.created_at,
        updatedAt: fileMetadata.updated_at,
        size: fileMetadata.size,
        fileId: fileMetadata.file_id,
    }
}

export function mapFileShare(fileShare: ServerFileShare) {
    if (!fileShare) {
        return null
    }

    return {
        id: fileShare.id,
        fileId: fileShare.file_id,
        userId: fileShare.user_id,
        permissions: mapFilePermissions(fileShare.permissions),
    }
}

export function mapFileShares(
    fileShares: { file_share: ServerFileShare; user: ServerUser }[],
) {
    return fileShares.map(fileShare => {
        return {
            fileShare: mapFileShare(fileShare.file_share),
            user: mapUser(fileShare.user),
        }
    })
}

export function mapFilePermission(filePermission: ServerFilePermission) {
    return {
        id: filePermission.id,
        name: filePermission.name,
        shareFileId: filePermission.share_file_id,
    }
}

export function mapFilePermissions(filePermissions: ServerFilePermission[]) {
    if (!filePermissions) {
        return []
    }
    return filePermissions.map(filePermission =>
        mapFilePermission(filePermission),
    )
}

export function mapFileShareLink(fileShareLink: ServerFileShareLink) {
    return {
        id: fileShareLink.id,
        fileId: fileShareLink.file_id,
        expiresAt: fileShareLink.expires_at,
        userId: fileShareLink.user_id,
    }
}
