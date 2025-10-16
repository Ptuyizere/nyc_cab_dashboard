<template>
    <div class="pagination">
        <button @click="$emit('prev')" :disabled="offset === 0">◀ Prev</button>
        <span>Showing {{ offset + 1 }}-{{ offset + limit }}</span>
        <button @click="$emit('next')">Next ▶</button>
    </div>
</template>

<script>
export default {
    props: ["limit", "offset"],
};
</script>

<style scoped>
.pagination {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    gap: 1rem;
    align-items: center;
}

button {
    padding: 0.4rem 1rem;
    border: none;
    border-radius: 5px;
    background-color: #d1d1d1;
    cursor: pointer;
}

button:hover {
    background-color: #bcbcbc;
}

button:disabled {
    background-color: #eee;
    cursor: not-allowed;
}
</style>