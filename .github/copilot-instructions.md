# AI Agent Instructions for Personal Portfolio

This document guides AI agents on effectively working with this personal portfolio website project.

## Project Overview

This is a static portfolio website built with HTML5, CSS3, and JavaScript, hosted on GitHub Pages. The site showcases professional work, skills, and experiences in a clean, responsive design.

## Key Architecture Points

- **Static Site Architecture**: No build tools or frameworks - pure HTML/CSS/JS
- **GitHub Pages Hosting**: Deployment happens automatically from the `main` branch
- **Asset Organization**: Follow the established directory structure:
  ```
  portfolio/
  ├── index.html          # Main entry point
  ├── css/               # Stylesheet directory
  ├── js/                # JavaScript directory
  └── assets/
      └── images/        # Image assets
  ```

## Development Workflow

1. **Local Development**:
   - Simply open `index.html` in a browser to preview changes
   - No build steps or server setup required

2. **Deployment**:
   - Commits to `main` branch automatically deploy to GitHub Pages
   - No additional deployment steps needed

## Project Conventions

### Code Style
- Use 2-space indentation for all files (HTML, CSS, JS)
- Follow semantic HTML5 practices
- Use CSS classes for styling, IDs for JavaScript hooks
- Prefer vanilla JavaScript - no external dependencies

### File Organization
- Keep image assets under `assets/images/`
- Maintain separate files for each major CSS component
- JavaScript files should be modular and focused

### Responsive Design
- Mobile-first approach
- Use responsive units (rem, em, %) over fixed pixels
- Standard breakpoints:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px

## Integration Points

1. **GitHub Pages**:
   - Site is hosted at `https://devanwyk.github.io/personal-portfolio`
   - DNS and HTTPS are handled automatically

2. **Contact Form** (if implemented):
   - Use client-side validation
   - Submit to a serverless function (TBD)

## Common Tasks

### Adding a New Project
1. Add project images to `assets/images/`
2. Update portfolio section in HTML
3. Add corresponding styles in CSS
4. Test responsive layout across devices

### Updating Content
- Main content edits happen in `index.html`
- Update metadata (title, description) for SEO
- Ensure images have proper alt text

## Need Help?

- Check the README.md for basic setup
- Review existing code for patterns
- Create issues for bugs or enhancements
- Contact: [@devanwyk](https://github.com/devanwyk)
