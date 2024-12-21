const files = 'files/share/link'

import { FileShareLinkRequestBuilder } from './builder'
import apiservice from '../service'
import { mapFileShareLink } from '../mapper'

export const createLink = async (
    createFileShareLink: FileShareLinkRequestBuilder,
) => {
    const res = await apiservice.post(files + '/', createFileShareLink.build())
    return {
        shareLink: mapFileShareLink(res.data.file_share_link),
    }
}

export const getShareLink = async (id: string) => {
    const res = await apiservice.get(files + '/' + id)
    return {
        shareLink: mapFileShareLink(res.data.share_link),
    }
}
