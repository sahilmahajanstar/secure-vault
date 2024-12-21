export class ProfileCreateRequestBuilder {
    user_id: string = ''
    profile_avatar: File | null = null

    build() {
        return {
            user_id: this.user_id,
            profile_avatar: this.profile_avatar,
        }
    }
}
