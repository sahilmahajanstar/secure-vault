import {
    mapFile,
    mapFileShare,
    mapFileShares,
    mapFiles,
    mapUsers,
} from '../mapper'

import { FileShareRequestBuilder } from './builder'
import apiservice from '../service'

const files = '/files/share'

export const searchUser = async ({
    fileId,
    email,
}: {
    fileId: string
    email: string
}) => {
    const res = await apiservice.get(files + '/search_user', {
        email,
        file_id: fileId,
    })
    return {
        users: mapUsers(res.data.users),
    }
}

export const shareFile = async (request: FileShareRequestBuilder) => {
    const res = await apiservice.post(files + '/', request.build())
    return {
        file: mapFile(res.data.file),
        fileShare: mapFileShares(res.data.file_shares),
    }
}

export const getFileShareUsers = async (fileId: string) => {
    const res = await apiservice.get(files, {
        file_id: fileId,
    })
    return {
        fileShareUsers: mapFileShares(res.data.file_shares),
        limit: res.data.limit,
        offset: res.data.offset,
        total: res.data.total,
    }
}

export const revokeAccess = async (fileShareId: string) => {
    const res = await apiservice.delete(files + '/' + fileShareId)
    return {
        fileShares: mapFileShare(res.data.file_share),
    }
}

export const getFilesSharedWithYou = async (query: {
    offset: number
    limit: number
}) => {
    const res = await apiservice.get(files + '/file_share_with_you', query)
    return {
        files: mapFiles(res.data.files),
        total: res.data.total,
        offset: res.data.offset,
        limit: res.data.limit,
    }
}
