describe("manipulating the todo list", () => {
    let uid     // user id
    let name    // name of the user (firstName + ' ' + lastName)
    let email   // email of the user

    beforeEach(() => {
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid
                name = user.firstName + ' ' + user.lastName
                email = user.email
                cy.visit('http://localhost:3000')
                cy.contains('div', 'Email Address').find('input[type=text]').type(email)
                cy.get('form').submit()
                cy.get('h1').should('contain.text', 'Your tasks, ' + name)
                cy.get(".submit-form").find("#title").type("Test task for Todos")
                cy.get(".submit-form").find("#url").type("PsLaI4jDftA")
                cy.get('[type="submit"]').click()
                cy.contains("Test task for Todos").click()
            })
        })

    })
    context("R8UC1 - Adding a todo item", () => {
        it("adds a new todo item when description is non-empty", () => {
            cy.get('.inline-form > [type="text"]').type("Take notes!!!")
            cy.get('.inline-form > [type="submit"]').click()
            cy.get('.todo-item').last().should('contain.text', 'Take notes!!!')
        })
        it("keeps the Add button disabled when description is empty", () => {
            cy.get('.inline-form > [type="submit"]').should("be.disabled")
        })
    })
    context("R8UC2 - Toggle todo item", () => {
        it("marks an active todo as done(struck through)", () => {
            cy.contains(".todo-item", "Watch video").find(".checker").click()
            cy.contains("Watch video").should('have.css', 'text-decoration-line', 'line-through')
        })
        it("marks a done todo as active again", () => {
            cy.contains(".todo-item", "Watch video").find(".checker").click()
            cy.contains("Watch video").should('have.css', 'text-decoration-line', 'line-through')
            cy.contains(".todo-item", "Watch video").find(".checker").click()
            cy.contains("Watch video").should('have.css', 'text-decoration-line', 'none')
        })
    })
    context("R8UC3 - Deleting todo item", () => {
        it("removes a todo when x is clicked", () => {
            cy.contains(".todo-item", "Watch video").find(".remover").click()
            cy.get(".todo-item").should("not.contain", "Watch video")
        })
        it("removes a todo from multiple when x is clicked", () => {
            cy.get('.inline-form > [type="text"]').type("Take notes!!!")
            cy.get('.inline-form > [type="submit"]').click()
            cy.contains(".todo-item", "Take notes!!!").find(".remover").click()
            cy.get(".todo-item").should("contain", "Watch video")
            cy.get(".todo-item").should("not.contain", "Take notes!!!")
        })
    })
    afterEach(() => {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})