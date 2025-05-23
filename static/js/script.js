// Project Filtering Functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectContainer = document.querySelector('#projects-container');
    
    // Add click event listener to each filter button
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get the filter value
            const filter = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Check if we should use client-side filtering or AJAX
            const projectCards = document.querySelectorAll('.project-card');
            
            if (projectCards.length > 0) {
                // Client-side filtering
                projectCards.forEach(card => {
                    // Add fade out animation
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.95)';
                    
                    setTimeout(() => {
                        if (filter === 'all' || card.getAttribute('data-category') === filter) {
                            card.style.display = 'block';
                            // Add fade in animation
                            setTimeout(() => {
                                card.style.opacity = '1';
                                card.style.transform = 'scale(1)';
                                // Ensure animation class is present
                                card.classList.add('animate-on-scroll');
                                card.classList.add('visible');
                            }, 50);
                        } else {
                            card.style.display = 'none';
                            // Remove animation classes
                            card.classList.remove('visible');
                        }
                    }, 300);
                });
            } else if (projectContainer) {
                // AJAX filtering
                fetch(`/?category=${filter}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    // Fade out current content
                    projectContainer.style.opacity = '0';
                    
                    setTimeout(() => {
                        // Clear the container
                        projectContainer.innerHTML = '';
                        
                        // Add the new projects
                        data.projects.forEach(project => {
                            const card = createProjectCard(project);
                            projectContainer.appendChild(card);
                        });
                        
                        // Fade in new content
                        setTimeout(() => {
                            projectContainer.style.opacity = '1';
                            
                            // Add animation classes to new cards
                            const newCards = document.querySelectorAll('.project-card');
                            newCards.forEach(card => {
                                card.classList.add('animate-on-scroll');
                                card.classList.add('visible');
                            });
                        }, 50);
                    }, 300);
                })
                .catch(error => console.error('Error loading projects:', error));
            }
        });
    });
    
    // Helper function to create project card elements
    function createProjectCard(project) {
        const card = document.createElement('div');
        card.className = 'project-card bg-gray-800 bg-opacity-50 rounded-xl overflow-hidden shadow-lg animate-on-scroll';
        card.setAttribute('data-category', project.category);
        
        let techStackHtml = '';
        if (project.tech_stack && project.tech_stack.length > 0) {
            techStackHtml = project.tech_stack.map(tech => 
                `<span class="tech-pill">${tech}</span>`
            ).join(' ');
        }
        
        card.innerHTML = `
            <div class="relative overflow-hidden" style="height: 200px;">
                <img src="${project.image_url}" alt="${project.title}" class="w-full h-full object-cover">
                <div class="absolute top-3 right-3 bg-purple-900 text-purple-100 text-xs px-2 py-1 rounded-full">
                    ${project.category_display}
                </div>
            </div>
            <div class="p-5">
                <h3 class="text-xl font-bold text-white mb-2">${project.title}</h3>
                <p class="text-gray-300 text-sm mb-3">${project.short_description}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    ${techStackHtml}
                </div>
                <div class="flex justify-between">
                    ${project.preview_url ? `<a href="${project.preview_url}" target="_blank" class="text-purple-400 hover:text-purple-300 text-sm flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        Demo
                    </a>` : ''}
                    ${project.code_url ? `<a href="${project.code_url}" target="_blank" class="text-purple-400 hover:text-purple-300 text-sm flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                        </svg>
                        Code
                    </a>` : ''}
                </div>
            </div>
        `;
        
        return card;
    }

    // For mobile responsiveness - adjust filter buttons layout
    function adjustFilterButtons() {
        const filterContainer = document.querySelector('.filter-container');
        if (filterContainer) {
            if (window.innerWidth < 640) { // Small screens
                filterContainer.classList.remove('gap-3');
                filterContainer.classList.add('gap-2');
            } else {
                filterContainer.classList.remove('gap-2');
                filterContainer.classList.add('gap-3');
            }
        }
    }

    // Call once on load
    adjustFilterButtons();
    
    // And on resize
    window.addEventListener('resize', adjustFilterButtons);
});

// Portfolio Initialization Functions
document.addEventListener("DOMContentLoaded", () => {
    // Particle initialization
    const particleCountHome = window.innerWidth < 768 ? 40 : 80;
    const particleCountContact = window.innerWidth < 768 ? 20 : 40;
    const particleCountOther = window.innerWidth < 768 ? 30 : 60;
    
    initParticles("particles-home", particleCountHome);
    initParticles("particles-contact", particleCountContact);
    initParticles("particles-about", particleCountOther);
    initParticles("particles-work", particleCountOther);
    initParticles("particles-projects", particleCountOther);
    initParticles("particles-skills", particleCountOther);
    initParticles("particles-education", particleCountOther);

    // Menu toggle
    initMenu();

    // Smooth scroll
    initSmoothScroll();

    // Form handling
    initForm();

    // Theme toggle
    initTheme();

    // Initialize scroll animations
    initScrollAnimations();
});

function initParticles(id, count) {
    if (document.getElementById(id)) {
        particlesJS(id, {
            particles: {
                number: { value: count, density: { enable: true, value_area: 800 } },
                color: { value: "#a855f7" },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: true },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 150, color: "#a855f7", opacity: 0.2, width: 1 },
                move: { enable: true, speed: 1, direction: "none", random: true, straight: false, out_mode: "out", bounce: false }
            },
            interactivity: {
                detect_on: "canvas",
                events: { onhover: { enable: true, mode: "grab" }, onclick: { enable: true, mode: "push" }, resize: true },
                modes: { grab: { distance: 140, line_linked: { opacity: 0.8 } }, push: { particles_nb: 4 } }
            },
            retina_detect: true
        });
    }
}

function initMenu() {
    document.getElementById("menu-toggle").addEventListener("click", () => {
        document.getElementById("mobile-menu").classList.toggle("hidden");
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", event => {
            event.preventDefault();
            document.querySelector(anchor.getAttribute("href")).scrollIntoView({ behavior: "smooth" });
            document.getElementById("mobile-menu").classList.add("hidden");
        });
    });
}

function initForm() {
    const form = document.getElementById("contactForm");
    if (form) {
        form.addEventListener("submit", event => {
            event.preventDefault();
            const data = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                subject: document.getElementById("subject").value,
                message: document.getElementById("message").value
            };
            console.log("Form submitted:", data);
            alert("Thanks for your message! I'll get back to you soon.");
            form.reset();
        });
    }
}

function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        if (savedTheme === 'light') {
            document.documentElement.classList.add('light-mode');
            themeToggle.checked = true;
        }
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.documentElement.classList.add('light-mode');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.classList.remove('light-mode');
                localStorage.setItem('theme', 'dark');
            }
        });
    }
}

function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // If the element has child elements with animate-on-scroll class
                const children = entry.target.querySelectorAll('.animate-on-scroll');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('visible');
                    }, index * 100); // Stagger the animations
                });
            }
        });
    }, {
        threshold: 0.15, // Trigger when 15% of the element is visible
        rootMargin: '0px'
    });

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    // Observe individual elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        observer.observe(element);
    });
}

// Cloudflare script (keeping for functionality)
(function() {
    function c() {
        var b = a.contentDocument || a.contentWindow.document;
        if (b) {
            var d = b.createElement('script');
            d.innerHTML = "window.__CF$cv$params={r:'935d27c58d3abfcc',t:'MTc0NTU3NjkyNS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";
            b.getElementsByTagName('head')[0].appendChild(d);
        }
    }
    if (document.body) {
        var a = document.createElement('iframe');
        a.height = 1;
        a.width = 1;
        a.style.position = 'absolute';
        a.style.top = 0;
        a.style.left = 0;
        a.style.border = 'none';
        a.style.visibility = 'hidden';
        document.body.appendChild(a);
        if ('loading' !== document.readyState) c();
        else if (window.addEventListener) document.addEventListener('DOMContentLoaded', c);
        else {
            var e = document.onreadystatechange || function() {};
            document.onreadystatechange = function(b) {
                e(b);
                'loading' !== document.readyState && (document.onreadystatechange = e, c());
            };
        }
    }
})(); 