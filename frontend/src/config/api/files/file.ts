import { mapFile, mapFiles } from '../mapper'

import { FileUploadRequestBuilder } from './builder'
import apiservice from '../service'

const files = '/files'

export const listFile = async (query: { offset: number; limit: number }) => {
    const res = await apiservice.get(files, query)
    return {
        files: mapFiles(res.data.files),
        total: res.data.total,
        offset: res.data.offset,
        limit: res.data.limit,
    }
}

export const uploadFile = async (
    file: FileUploadRequestBuilder,
    onUploadProgress: (progressEvent: { progress: number }) => void,
) => {
    const res = await apiservice.post(files + '/', await file.build(), {
        onUploadProgress,
    })
    return {
        files: mapFiles(res.data.files),
    }
}

export const downloadFile = async (
    fileId: string,
    {
        includeFile,
        authenticated,
        includeFileShare,
    }: {
        includeFile: boolean
        authenticated: boolean
        includeFileShare: boolean
    },
) => {
    let res
    if (authenticated) {
        res = await apiservice.get(files + '/' + fileId, {
            include_file: String(includeFile),
            include_file_share: String(includeFileShare),
        })
    } else {
        res = await apiservice.get(files + '/' + fileId + '/public/', {
            include_file: String(includeFile),
            include_file_share: String(includeFileShare),
        })
    }
    return {
        file: mapFile(res.data.file),
        data: res.data.file_data,
    }
}

export const deleteFile = async (fileId: string) => {
    const res = await apiservice.delete(files + '/' + fileId)
    return {
        file: mapFile(res.data.file),
    }
}
