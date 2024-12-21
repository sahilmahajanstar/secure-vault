import '../style/listFile.css'

import React, { useCallback, useEffect } from 'react'

import { File } from '../type/file'
import { FileTable } from './FileTable'
import { GridRenderCellParams } from '@mui/x-data-grid'
import { fileShareApi } from '../../config/api/files'
import { useAppSelector } from '../../config/redux/hooks'

const ShareWithYou: React.FC = () => {
    const [files, setFiles] = React.useState<File[]>([])
    const user = useAppSelector(state => state.user.user)
    const [total, setTotal] = React.useState<number>(0)
    const listFiles = useCallback(async (offset: number, limit: number) => {
        const res = await fileShareApi.getFilesSharedWithYou({ offset, limit })
        setFiles(res.files)
        setTotal(res.total)
        return res
    }, [])

    useEffect(() => {
        listFiles(0, 10)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
    const columns =
        user?.role === 'admin'
            ? [
                  {
                      field: 'owner',
                      headerName: 'Owner name',
                      flex: 1,
                      filterable: false,
                      sortable: false,
                      headerClassName: 'header-table',
                      renderCell: (params: GridRenderCellParams) =>
                          params.row.user.firstName +
                          ' ' +
                          params.row.user.lastName,
                  },
              ]
            : []
    if (files.length === 0) {
        return (
            <h1
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '90vh',
                }}>
                Nothing has shared with you
            </h1>
        )
    }
    return (
        <div>
            <FileTable
                rowCount={total}
                columns={columns}
                files={files}
                reloadList={listFiles}
            />
        </div>
    )
}

export default ShareWithYou
