// Leads Management System - Main JavaScript Application

class LeadsManager {
    constructor() {
        this.users = [];
        this.filteredUsers = [];
        this.filterOptions = {};
        this.dataTable = null;
        this.init();
    }

    // Initialize the application
    init() {
        this.setupEventListeners();
        this.loadFilterOptions();
        this.loadUsers();
    }

    // Setup event listeners
    setupEventListeners() {
        // Filter inputs
        $('#searchInput').on('input', this.debounce(() => this.applyFilters(), 300));
        $('#locationFilter, #schoolFilter, #countryFilter, #sourceFilter').on('change', () => this.applyFilters());
        
        // Clear filters button
        $('#clearFilters').on('click', () => this.clearFilters());
        
        // Table row click handler
        $(document).on('click', '.user-row', (e) => {
            const uid = $(e.currentTarget).data('uid');
            this.showUserDetail(uid);
        });
    }

    // Debounce function for search input
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Show loading spinner
    showLoading() {
        $('#loadingSpinner').show();
    }

    // Hide loading spinner
    hideLoading() {
        $('#loadingSpinner').hide();
    }

    // Load filter options from API
    async loadFilterOptions() {
        try {
            const response = await fetch('/api/filters');
            if (!response.ok) throw new Error('Failed to load filter options');
            
            this.filterOptions = await response.json();
            this.populateFilterDropdowns();
        } catch (error) {
            console.error('Error loading filter options:', error);
            this.showError('Failed to load filter options');
        }
    }

    // Populate filter dropdowns
    populateFilterDropdowns() {
        // Populate location filter
        const locationSelect = $('#locationFilter');
        locationSelect.empty().append('<option value="">All Locations</option>');
        this.filterOptions.locations.forEach(location => {
            locationSelect.append(`<option value="${location}">${location}</option>`);
        });

        // Populate school filter
        const schoolSelect = $('#schoolFilter');
        schoolSelect.empty().append('<option value="">All Schools</option>');
        this.filterOptions.schools.forEach(school => {
            schoolSelect.append(`<option value="${school}">${school}</option>`);
        });

        // Populate country filter
        const countrySelect = $('#countryFilter');
        countrySelect.empty().append('<option value="">All Countries</option>');
        this.filterOptions.countries.forEach(country => {
            countrySelect.append(`<option value="${country}">${country}</option>`);
        });
    }

    // Load users from API
    async loadUsers() {
        this.showLoading();
        try {
            const response = await fetch('/api/users');
            if (!response.ok) throw new Error('Failed to load users');
            
            this.users = await response.json();
            this.filteredUsers = [...this.users];
            this.renderUsersTable();
            this.updateUserCount();
            this.updateStatistics();
        } catch (error) {
            console.error('Error loading users:', error);
            this.showError('Failed to load users data');
        } finally {
            this.hideLoading();
        }
    }

    // Apply filters to users
    async applyFilters() {
        const filters = {
            search: $('#searchInput').val(),
            location_filter: $('#locationFilter').val(),
            school_filter: $('#schoolFilter').val(),
            country_filter: $('#countryFilter').val(),
            source_filter: $('#sourceFilter').val()
        };

        // Build query string
        const queryParams = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) queryParams.append(key, value);
        });

        this.showLoading();
        try {
            const response = await fetch(`/api/users?${queryParams}`);
            if (!response.ok) throw new Error('Failed to apply filters');
            
            this.filteredUsers = await response.json();
            this.renderUsersTable();
            this.updateUserCount();
            this.updateStatistics();
        } catch (error) {
            console.error('Error applying filters:', error);
            this.showError('Failed to apply filters');
        } finally {
            this.hideLoading();
        }
    }

    // Clear all filters
    clearFilters() {
        $('#searchInput').val('');
        $('#locationFilter').val('');
        $('#schoolFilter').val('');
        $('#countryFilter').val('');
        $('#sourceFilter').val('');
        this.loadUsers();
    }

    // Render users table
    renderUsersTable() {
        // Destroy existing DataTable if it exists
        if (this.dataTable) {
            this.dataTable.destroy();
            this.dataTable = null;
        }

        const tbody = $('#usersTable tbody');
        tbody.empty();

        if (this.filteredUsers.length === 0) {
            tbody.append(this.createEmptyStateRow());
            // Initialize DataTable even for empty state
            this.dataTable = $('#usersTable').DataTable({
                paging: false,
                searching: false,
                ordering: false,
                info: false,
                responsive: true,
                language: {
                    emptyTable: "No users found matching the current filters"
                }
            });
            return;
        }

        this.filteredUsers.forEach(user => {
            const row = this.createUserRow(user);
            tbody.append(row);
        });

        // Initialize DataTable with data
        this.dataTable = $('#usersTable').DataTable({
            paging: true,
            pageLength: 25,
            searching: false, // We handle search manually
            ordering: true,
            info: true,
            responsive: true,
            language: {
                emptyTable: "No users found matching the current filters"
            }
        });
    }

    // Create empty state row
    createEmptyStateRow() {
        return `
            <tr>
                <td colspan="8" class="text-center empty-state">
                    <i class="fas fa-users fa-3x mb-3"></i>
                    <h5>No users found</h5>
                    <p class="text-muted">Try adjusting your filters or search criteria</p>
                </td>
            </tr>
        `;
    }

    // Create user row
    createUserRow(user) {
        const avatar = user.linkedin_image_url 
            ? `<img src="${user.linkedin_image_url}" alt="${user.user_name}" class="user-avatar">`
            : `<div class="user-avatar-placeholder">${user.user_name.charAt(0).toUpperCase()}</div>`;

        const linkedinLink = user.linkedin_profile_url 
            ? `<a href="${user.linkedin_profile_url}" target="_blank" class="linkedin-link" onclick="event.stopPropagation();">
                 <i class="fab fa-linkedin"></i> Profile
               </a>`
            : '<span class="text-muted">No LinkedIn</span>';

        const sourceBadge = this.getSourceBadge(user.source_category);

        return `
            <tr class="user-row ${user.color_class}" data-uid="${user.uid}">
                <td>${avatar}</td>
                <td>
                    <div class="fw-semibold">${user.user_name}</div>
                    ${linkedinLink}
                </td>
                <td>${user.title}</td>
                <td>${user.location}</td>
                <td>${user.req_school}</td>
                <td>${user.req_country}</td>
                <td>${sourceBadge}</td>
                <td>
                    <button class="btn btn-primary btn-sm btn-action" onclick="event.stopPropagation(); leadsManager.showUserDetail('${user.uid}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                </td>
            </tr>
        `;
    }

    // Get source badge HTML
    getSourceBadge(sourceCategory) {
        const badges = {
            'schools_only': '<span class="badge bg-info source-badge">Schools Only</span>',
            'salesnav_only': '<span class="badge bg-warning source-badge">Sales Navigator</span>',
            'both': '<span class="badge bg-success source-badge">Both Tables</span>'
        };
        return badges[sourceCategory] || '<span class="badge bg-secondary source-badge">Unknown</span>';
    }

    // Show user detail modal
    async showUserDetail(uid) {
        this.showLoading();
        try {
            const response = await fetch(`/api/users/${uid}`);
            if (!response.ok) throw new Error('Failed to load user details');
            
            const userDetail = await response.json();
            this.renderUserDetailModal(userDetail);
            
            const modal = new bootstrap.Modal(document.getElementById('userDetailModal'));
            modal.show();
        } catch (error) {
            console.error('Error loading user details:', error);
            this.showError('Failed to load user details');
        } finally {
            this.hideLoading();
        }
    }

    // Render user detail modal
    renderUserDetailModal(user) {
        const modalTitle = document.getElementById('userDetailModalLabel');
        modalTitle.textContent = `${user.user_name} - Detailed Information`;

        const modalBody = document.getElementById('userDetailContent');
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center mb-3">
                    ${user.linkedin_image_url 
                        ? `<img src="${user.linkedin_image_url}" alt="${user.user_name}" class="img-fluid rounded-circle mb-3" style="max-width: 150px;">`
                        : `<div class="user-avatar-placeholder mx-auto mb-3" style="width: 100px; height: 100px; font-size: 2rem;">${user.user_name.charAt(0).toUpperCase()}</div>`
                    }
                    <h5>${user.user_name}</h5>
                    <p class="text-muted">${user.title}</p>
                    ${user.linkedin_profile_url 
                        ? `<a href="${user.linkedin_profile_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                             <i class="fab fa-linkedin"></i> LinkedIn Profile
                           </a>`
                        : ''
                    }
                </div>
                <div class="col-md-8">
                    <div class="user-detail-section">
                        <h6><i class="fas fa-info-circle me-2"></i>Basic Information</h6>
                        <div class="detail-row">
                            <div class="row">
                                <div class="col-sm-4 detail-label">Location:</div>
                                <div class="col-sm-8 detail-value">${user.location}</div>
                            </div>
                        </div>
                        <div class="detail-row">
                            <div class="row">
                                <div class="col-sm-4 detail-label">School:</div>
                                <div class="col-sm-8 detail-value">${user.req_school}</div>
                            </div>
                        </div>
                        <div class="detail-row">
                            <div class="row">
                                <div class="col-sm-4 detail-label">Country:</div>
                                <div class="col-sm-8 detail-value">${user.req_country}</div>
                            </div>
                        </div>
                    </div>

                    ${user.headline ? `
                        <div class="user-detail-section">
                            <h6><i class="fas fa-quote-left me-2"></i>Headline</h6>
                            <p class="detail-value">${user.headline}</p>
                        </div>
                    ` : ''}

                    ${user.about ? `
                        <div class="user-detail-section">
                            <h6><i class="fas fa-user me-2"></i>About</h6>
                            <p class="detail-value">${user.about}</p>
                        </div>
                    ` : ''}

                    ${user.skills ? `
                        <div class="user-detail-section">
                            <h6><i class="fas fa-cogs me-2"></i>Skills</h6>
                            <p class="detail-value">${user.skills}</p>
                        </div>
                    ` : ''}

                    ${user.experience ? `
                        <div class="user-detail-section">
                            <h6><i class="fas fa-briefcase me-2"></i>Experience</h6>
                            <p class="detail-value">${user.experience}</p>
                        </div>
                    ` : ''}

                    <div class="user-detail-section">
                        <h6><i class="fas fa-database me-2"></i>Data Source</h6>
                        <div class="detail-row">
                            <div class="row">
                                <div class="col-sm-4 detail-label">Schools Table:</div>
                                <div class="col-sm-8">
                                    ${user.in_schools_table 
                                        ? `<span class="badge bg-success">Yes</span> ${user.schools_timestamp ? `<small class="text-muted ms-2">${user.schools_timestamp}</small>` : ''}`
                                        : '<span class="badge bg-secondary">No</span>'
                                    }
                                </div>
                            </div>
                        </div>
                        <div class="detail-row">
                            <div class="row">
                                <div class="col-sm-4 detail-label">Sales Navigator:</div>
                                <div class="col-sm-8">
                                    ${user.in_salesnav_table 
                                        ? `<span class="badge bg-success">Yes</span> ${user.salesnav_timestamp ? `<small class="text-muted ms-2">${user.salesnav_timestamp}</small>` : ''}`
                                        : '<span class="badge bg-secondary">No</span>'
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Update user count
    updateUserCount() {
        const count = this.filteredUsers.length;
        const total = this.users.length;
        $('#userCount').text(`${count} of ${total} users`);
    }

    // Update statistics
    updateStatistics() {
        const stats = this.calculateStatistics();
        $('#totalUsers').text(stats.total);
        $('#schoolsOnlyCount').text(stats.schoolsOnly);
        $('#salesnavOnlyCount').text(stats.salesnavOnly);
        $('#bothTablesCount').text(stats.bothTables);
    }

    // Calculate statistics from filtered users
    calculateStatistics() {
        const stats = {
            total: this.filteredUsers.length,
            schoolsOnly: 0,
            salesnavOnly: 0,
            bothTables: 0
        };

        this.filteredUsers.forEach(user => {
            switch(user.source_category) {
                case 'schools_only':
                    stats.schoolsOnly++;
                    break;
                case 'salesnav_only':
                    stats.salesnavOnly++;
                    break;
                case 'both':
                    stats.bothTables++;
                    break;
            }
        });

        return stats;
    }

    // Show error message
    showError(message) {
        const errorDiv = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Add to top of container
        $('.container').prepend(errorDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            $('.alert').alert('close');
        }, 5000);
    }
}

// Initialize the application when the document is ready
$(document).ready(() => {
    window.leadsManager = new LeadsManager();
});
