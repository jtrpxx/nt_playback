<template>
    <NotFound v-if="notFound" />
    <UserForm v-else-if="loaded" :mode="'edit'" :initialData="initialData" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserForm from './UserForm.vue'
import NotFound from './NotFound.vue'
import { API_GET_USER_PROFILE } from '../api/paths'


const route = useRoute()
const router = useRouter()
const initialData = ref(null)
const loaded = ref(false)
const notFound = ref(false)

onMounted(async () => {
    const id = route.params.id
    if (!id) {
        router.replace('/user-management')
        return
    }
    try {
        const res = await fetch(API_GET_USER_PROFILE(id), { credentials: 'include' })
        let json = null
        try { json = await res.json() } catch (e) { }

        if (json?.message === 'User not found.') {
            notFound.value = true
            loaded.value = true
            return
        }

        await import('../assets/css/add-user.css')

        initialData.value = json
        loaded.value = true
    } catch (e) {
        console.error('Error fetching profile', e)
        router.replace('/user-management')
    }
})
</script>
