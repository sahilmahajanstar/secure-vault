import { User } from '../../../users/type/user'
import { encryptFile } from '../../../utils/webCrypto'

export class FileUploadRequestBuilder {
    files: File[] = []
    key: CryptoKey | null = null

    setFiles(files: File[]) {
        this.files = files
    }

    setKey(key: CryptoKey) {
        this.key = key
    }

    async formatFiles() {
        return Promise.all(
            this.files.map(async file => {
                return {
                    file_name: file.name,
                    file_size: file.size,
                    content_type: file.type,
                    share_type: 'private',
                    data: await encryptFile(file),
                    is_favorite: false,
                }
            }),
        )
    }

    async build() {
        return {
            files: await this.formatFiles(),
            key: this.key,
        }
    }
}

export class FileShareRequestBuilder {
    file_id: string = ''
    share_type: 'private' | 'public' = 'private'
    users: {
        id: string
        permissions: {
            id: string
            name: string
        }[]
    }[] = []

    setFileId(fileId: string) {
        this.file_id = fileId
        return this
    }

    setUsers(users: User[], permissions: string[]) {
        if (users.length !== 0 && permissions.length === 0) {
            throw new Error('Permissions are required')
        }
        this.users = users.map(user => ({
            id: user.id,
            permissions: permissions.map(permission => {
                return {
                    id: permission,
                    name: permission,
                }
            }),
        }))
        return this
    }

    setShareType(shareType: 'private' | 'public') {
        this.share_type = shareType
        return this
    }

    build() {
        return {
            file_id: this.file_id,
            share_type: this.share_type,
            users: this.users,
        }
    }
}

export class FileShareLinkRequestBuilder {
    file_id: string = ''
    expires_in_hours: number = 24

    setFileId(fileId: string) {
        this.file_id = fileId
        return this
    }

    setExpiresInHours(expiresInHours: number) {
        this.expires_in_hours = expiresInHours
        return this
    }

    build() {
        return {
            file_id: this.file_id,
            expires_in_hours: this.expires_in_hours,
        }
    }
}
