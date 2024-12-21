export const If = ({
    condition,
    children,
}: {
    condition?: boolean | string | null
    children: React.ReactNode
}) => {
    if (condition) {
        return children
    }
    return null
}
