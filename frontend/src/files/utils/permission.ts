import { File } from '../../files/type/file'
import { FilePermissions } from '../type/file'
import { User } from '../../users/type/user'
export const hasPermission = (
    permission: string,
    file: File,
    user: User,
    permissions: FilePermissions[],
) => {
    if (permission === 'view' && file?.shareType === 'public') return true
    if (user && user.role === 'admin') return true
    if (file?.userId.replaceAll('-', '') === user?.id.replaceAll('-', ''))
        return true
    // for private
    for (const p of permissions) {
        if (p.name === permission) {
            return true
        }
    }
    return false
}
