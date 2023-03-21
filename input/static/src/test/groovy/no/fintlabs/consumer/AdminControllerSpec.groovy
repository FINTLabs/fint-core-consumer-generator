package no.fintlabs.consumer

import no.fintlabs.cache.CacheManager
import no.fintlabs.consumer.admin.AdminController
import no.fintlabs.core.consumer.shared.ConsumerProps
import no.fintlabs.core.consumer.shared.resource.CacheService
import spock.lang.Specification

class AdminControllerSpec extends Specification {
    def "Check given organisations"() {
        given:
        def service1 = Mock(CacheService) { getCacheUrn() >> "TestValue1" }
        def service2 = Mock(CacheService) { getCacheUrn() >> "TestValue2" }
        def adminController = new AdminController(Mock(ConsumerProps), Mock(CacheManager))
        adminController.consumerServices = [service1, service2]

        when:
        def result = adminController.getOrganisations()

        then:
        result
        result.size() == 2
        result.getAt(0) == "TestValue1"
        result.getAt(1) == "TestValue2"
    }

    def "Check given assets"() {
        given:
        ConsumerProps consumerProps = Mock() {
            orgId >> "MittFylke.no"
        }
        def adminController = new AdminController(consumerProps, Mock(CacheManager))

        when:
        String result = adminController.getAssets()

        then:
        result.contains("MittFylke.no")
        !result.contains(",")
    }

    def "Check given caches"() {
        given:
        def service1 = Mock(CacheService) {
            getCacheUrn() >> "urn:fintlabs.no:test.no:cache1";
            getCacheSize() >> 58
        }
        def service2 = Mock(CacheService) {
            getCacheUrn() >> "urn:fintlabs.no:test.no:cache2";
            getCacheSize() >> 179
        }
        def adminController = new AdminController(Mock(ConsumerProps), Mock(CacheManager))
        adminController.consumerServices = [service1, service2]

        when:
        def result = adminController.getCaches()

        then:
        result
        result.size() == 2
        result.get("urn:fintlabs.no:test.no:cache1") == 58
        result.get("urn:fintlabs.no:test.no:cache2") == 179
    }
}
